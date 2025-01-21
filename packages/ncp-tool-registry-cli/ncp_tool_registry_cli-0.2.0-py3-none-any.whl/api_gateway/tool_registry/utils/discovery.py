import logging
from typing import List
import requests

from urllib.parse import urljoin
from metatron.http import MetatronAdapter

logger = logging.getLogger(__name__)


def get_app_name(base_url: str) -> str:
    if "://" not in base_url:
        return base_url.split(".")[0].split("-")[0]
    return base_url.split("://")[1].split(".")[0].split("-")[0]


def discover_openapi(base_url: str):
    session = requests.Session()
    if "netflix" in base_url:
        session.mount("https://", MetatronAdapter(get_app_name(base_url)))
        print(f"Mounted MetatronAdapter for {get_app_name(base_url)}")

    discovery_paths = [
        "/admin/swagger/v1/api-docs",
        "/admin/swagger/v2/api-docs",
        "/admin/swagger/v3/api-docs",
        "/admin/v3/api-docs",
        "/admin/swagger/api-docs",
        "/admin/swagger.json",
        "/swagger.json",
        "/openapi.json",
        "/api-docs",
        "/swagger/v1/swagger.json",
        "/api/swagger.json",
        "/api/v1/swagger.json",
        "/api/v2/swagger.json",
        "/api/documentation",
        "/docs/swagger.json",
        "/docs/openapi.json",
        "/openapi/swagger.json",
        "/swagger-ui/swagger.json",
        "/api-docs/swagger.json",
        "/spec/swagger.json",
        "/v1/swagger.json",
        "/v2/swagger.json",
        "/swagger/docs/v1",
        "/swagger/docs/v2",
        "/swagger/v1/api-docs",
        "/swagger/v2/api-docs",
        "/swagger/v3/api-docs",
        "/.well-known/openapi.json",
        "/.well-known/swagger.json",
    ]

    for path in discovery_paths:
        try:
            full_url = urljoin(base_url, path)
            response = session.get(full_url)
            if response.ok:
                return response.json()
        except Exception:
            continue

    logger.warning(f"Could not find OpenAPI docs for {base_url}")
    return None


def get_endpoint_paths(base_url=None, spec=None):
    if not spec:
        spec = discover_openapi(base_url)

    return list(spec.get("paths", {}))


def get_path_methods(path, base_url=None, spec=None):
    if not spec:
        spec = discover_openapi(base_url)

    return list(spec.get("paths", {}).get(path, {}))


def get_endpoint_schemas_and_components(path: str, methods: List[str], base_url=None, spec=None):
    if not spec:
        spec = discover_openapi(base_url)

    path_details = spec["paths"].get(path, {})
    if not path_details:
        raise Exception("No method found for path")

    components = {"schemas": {}}
    request_schemas = {}
    response_schemas = {}

    for method in methods:
        if method.lower() in path_details:
            method_schema = path_details[method].copy()
            responses = method_schema.pop("responses", None)
            response_schemas[method] = responses

            if "summary" not in method_schema:
                method_schema["summary"] = input("Method summary could not be found automatically. Please add a method summary: ")

            request_schemas[method] = method_schema

            method_components = get_used_components(method_schema, spec["components"])
            if responses:
                response_components = get_used_components(responses, spec["components"])
                method_components["schemas"].update(response_components["schemas"])

            components["schemas"].update(method_components["schemas"])

    return request_schemas, components, response_schemas


def extract_refs(obj):
    refs = set()
    if isinstance(obj, dict):
        for key, value in obj.items():
            if key == "$ref" and isinstance(value, str):
                if value.startswith("#/components/schemas/"):
                    refs.add(value.split("/")[-1])
            refs.update(extract_refs(value))
    elif isinstance(obj, list):
        for item in obj:
            refs.update(extract_refs(item))
    return refs


def get_used_components(path_operation_schema, all_components):
    refs = extract_refs(path_operation_schema)
    used_components = {"schemas": {}}
    processed = set()

    def process_component(component_name):
        if component_name in processed:
            return
        processed.add(component_name)

        if component_name in all_components["schemas"]:
            used_components["schemas"][component_name] = all_components["schemas"][component_name]
            nested_refs = extract_refs(all_components["schemas"][component_name])
            for nested_ref in nested_refs:
                process_component(nested_ref)

    for ref in refs:
        process_component(ref)

    return used_components
