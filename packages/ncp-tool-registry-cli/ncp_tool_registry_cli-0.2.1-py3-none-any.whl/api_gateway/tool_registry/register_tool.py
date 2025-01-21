import click
from pydantic import ValidationError

from api_gateway.models.tool_models import Info, RegistryTool, Permissions, GenAIProject
from api_gateway.tool_registry.tool_registry_operations import ToolRegistryOperations
from api_gateway.tool_registry.utils.discovery import (
    discover_openapi,
    get_app_name,
    get_endpoint_paths,
    get_path_methods,
    get_endpoint_schemas_and_components,
)
from api_gateway.tool_registry.utils.ncp_project_connection import get_gandalf_policy_from_ncp_project
from api_gateway.tool_registry.utils.validators import is_valid_id, is_valid_jsonpath
from api_gateway.gateway_service import process_schema

tool_ops = ToolRegistryOperations()


@click.group()
def cli():
    pass


@cli.command()
def create_tool():
    tool_ops.sync_registry()
    tool = build_tool_request()
    if tool:
        try:
            print("-" * 20)
            print("Uploading tool to ConfigBin...")
            tool = tool_ops.add_tool(tool=tool, sync_to_danswer=False)
            print("Done uploading tool to ConfigBin...")
            print("-" * 20)

            danswer_sync = input("Sync tool to Danswer? (y/n): ")
            while danswer_sync.lower() not in ["y", "n"]:
                danswer_sync = input("Please enter 'y' or 'n': ")

            if danswer_sync.lower() == "y":
                print("Syncing tool to Danswer...")
                tool_ops.sync_tool_to_danswer(tool.tool_id)
                print("Done adding tool to Danswer")

            print("-" * 20)
            print("Tool registration complete!")

        except Exception as e:
            print(f"Error registering tool: {e}")
            return


def get_tool_id_from_user() -> str:
    print("\n--- Tool ID ---")
    tool_id = input("\nEnter tool id: ").strip()
    while tool_ops.get_tool(tool_id, ignore_error=True) or not is_valid_id(tool_id):
        if tool_ops.get_tool(tool_id, ignore_error=True):
            print(f"Tool ID {tool_id} already exists! Please choose a different tool id.\n")
        if not is_valid_id(tool_id):
            print("Invalid tool id! Please use only alphanumeric characters, underscores, and dashes.\n")
        tool_id = input("Enter tool id: ").strip()
    return tool_id


def get_ncp_project_from_user() -> str:
    print("\n--- NCP Project ---")
    print(
        "Connecting to an existing NCP project is required to register a tool. Access control for the tool will use the NCP project's Gandalf policy."
    )
    ncp_env = input("Enter the environment your NCP project is in. Either 'test' or 'prod': ").strip()
    while ncp_env not in ["test", "prod"]:
        ncp_env = input("Please only enter either 'test' or 'prod': ").strip()
    ncp_project_id = input("Enter NCP project id: ").strip()
    while True:
        gandalf_policy = get_gandalf_policy_from_ncp_project(ncp_project_id, ncp_env)
        if gandalf_policy:
            print(f"Successfully found project and fetched Gandalf policy: {gandalf_policy}")
            return ncp_env, ncp_project_id, gandalf_policy
        ncp_project_id = input("Could not fetch Gandalf policy for given NCP project id. Please enter another NCP project id: ").strip()


def get_info_from_user() -> Info:
    print("\n--- Tool Info ---")
    title = input("Enter title: ").strip()
    description = input("Enter description: ").strip()
    version = input("Enter version: ").strip()
    return Info(title=title, description=description, version=version)


def get_path_and_method_from_user() -> tuple:
    print("\n--- Request Schema ---")
    base_url = input("Please enter the base URL (include port): ").strip()
    spec = discover_openapi(base_url)
    while not spec:
        print("Couldn't get OpenAPI docs from given URL. Please try another URL.")
        base_url = input("Please enter the base URL (include port): ").strip()
        spec = discover_openapi(base_url)

    paths = get_endpoint_paths(spec=spec)
    print("\nAvailable paths:")
    for idx, path in enumerate(paths, 1):
        print(f"{idx}. {path}")

    selected_path = input("\nPlease enter a path or number from the list above: ").strip()
    if selected_path.isdigit() and int(selected_path) <= len(paths):
        selected_path = paths[int(selected_path) - 1]
    else:
        while selected_path not in paths:
            print("\nPath not in list above!")
            selected_path = input("Please enter a path from the list above: ").strip()

    methods = get_path_methods(spec=spec, path=selected_path)
    print("\nAvailable methods:")
    for method in methods:
        print(f"- {method}")

    selected_methods = input("\nPlease enter comma-separated methods (e.g., get,post): ").strip().lower()
    while not selected_methods:
        print("\nPlease select at least one method!")
        selected_methods = input("Please enter comma-separated methods (e.g., get,post): ").strip().lower()
    selected_methods = [m.strip() for m in selected_methods.split(",")]
    print("Selected methods: ", selected_methods)
    return base_url, selected_path, selected_methods, spec


def get_jsonpaths_from_user(request_schemas: dict) -> tuple:
    print("\n--- Pre/postprocessing Queries ---")
    preprocessing_jsonpath = input("\nEnter preprocessing jsonpath (or press Enter for empty string): ").strip()
    while preprocessing_jsonpath and (
        not is_valid_jsonpath(preprocessing_jsonpath) or type(process_schema(request_schemas, preprocessing_jsonpath)) is not dict
    ):
        print("\nInvalid jsonpath string!")
        preprocessing_jsonpath = input("Enter preprocessing jsonpath (or press Enter for empty string): ").strip()

    postprocessing_jsonpath = input("\nEnter postprocessing jsonpath (or press Enter for empty string): ").strip()
    while postprocessing_jsonpath and not is_valid_jsonpath(postprocessing_jsonpath):
        print("\nInvalid jsonpath string!")
        postprocessing_jsonpath = input("Enter postprocessing jsonpath (or press Enter for empty string): ").strip()
    return preprocessing_jsonpath, postprocessing_jsonpath


def get_tool_accessibility_from_user() -> str:
    print("\n--- Tool Accessibility ---")
    print("Only those under the owner NCP project's Gandalf policy can update or delete tools, regardless of accessibility.")
    print(
        "Public tools can be invoked by any user, while protected tools can only be invoked by those with access to the allowed projects you specify."
    )
    # visbility = input(
    #     "If you want to make the tool private, enter 'private'. Input anything else or press Enter to make the tool public: "
    # ).strip()
    # return visbility.lower() == "private"
    accessibility = input("Enter 'protected' to restrict access, or press Enter for public: ").strip().lower()
    is_protected = accessibility == "protected"

    allowed_projects = []
    if is_protected:
        print("\nAdd projects that should have access to this tool (press Enter without input when done).")
        print("All users with access to these projects will be able to invoke the tool.")
        print("Unless they have access to the owner project, they will NOT be able to update or delete the tool in the future.")
        while True:
            ncp_env = input("\nEnter project environment (test/prod) or press Enter to finish: ").strip().lower()
            if not ncp_env:
                break

            if ncp_env not in ["test", "prod"]:
                print("Please enter either 'test' or 'prod' only.")
                continue

            project_id = input("Enter NCP project id: ").strip()
            if (project_id, ncp_env) in [(p.project_id, p.env) for p in allowed_projects]:
                print("Project already added to allowed list.")
                continue

            gandalf_policy = get_gandalf_policy_from_ncp_project(project_id, ncp_env)
            if gandalf_policy:
                allowed_projects.append(GenAIProject(env=ncp_env, project_id=project_id, gandalf_policy=gandalf_policy))
                print(f"Added project {project_id} ({ncp_env}) to allowed list.")
            else:
                print("Could not fetch Gandalf policy for given project. Project not added.")

    return "protected" if is_protected else "public", allowed_projects


def build_tool_request() -> RegistryTool:
    print("\nLet's register your custom tool! Please provide the following information:")
    tool_id = get_tool_id_from_user()

    owner_env, owner_project_id, owner_gandalf_policy = get_ncp_project_from_user()
    owner_ncp_project = GenAIProject(env=owner_env, project_id=owner_project_id, gandalf_policy=owner_gandalf_policy)

    info = get_info_from_user()

    base_url, selected_path, selected_methods, spec = get_path_and_method_from_user()
    invocation = {"endpoint": base_url + selected_path}
    if "netflix" in base_url:
        invocation["type"] = "metatron_endpoint"
        invocation["app_name"] = get_app_name(base_url)

    request_schemas, components, response_schemas = get_endpoint_schemas_and_components(
        path=selected_path, methods=selected_methods, spec=spec
    )
    preprocessing_jsonpath, postprocessing_jsonpath = get_jsonpaths_from_user(request_schemas)

    if preprocessing_jsonpath:
        # Currently doing this here so LLM generates request with preprocessing applied (instead of generating full request and then preprocessing)
        request_schemas = process_schema(request_schemas, preprocessing_jsonpath)

    accessibility, allowed_projects = get_tool_accessibility_from_user()
    permissions = Permissions(owner=owner_ncp_project, accessibility=accessibility, allowed_projects=allowed_projects)

    try:
        return RegistryTool(
            tool_id=tool_id,
            info=info,
            openapi=spec["openapi"],
            permissions=permissions,
            invocation=invocation,
            request_schema=request_schemas,
            preprocessing_jsonpath=preprocessing_jsonpath,
            response_schema=response_schemas,
            postprocessing_jsonpath=postprocessing_jsonpath,
            components=components,
        )
    except ValidationError as e:
        print(f"\nError creating tool request: {e}")
        return None


if __name__ == "__main__":
    cli()
