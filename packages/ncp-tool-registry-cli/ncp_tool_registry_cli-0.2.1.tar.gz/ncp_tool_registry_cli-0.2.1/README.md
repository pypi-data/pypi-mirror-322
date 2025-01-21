# Tool Registry + API Gateway

[Gen AI Tool Design Doc](https://docs.google.com/document/d/11NONHT0bLBNZ3XFhQ7p2YGn8MoPAXrFAJfIaNR09RcQ/edit?usp=sharing)

## How to Use Tools in Danswer/Chat2
#### REGISTERED TOOLS ARE CURRENTLY ONLY AVAILABLE IN TEST: https://chat2.test.netflix.net/chat

1. **Create New Assistant**: Go to Manage Assistants -> Create New Assistant and specify the name, description, and instructions.

2. **Add Tool**: Select your tool under the Capabilities section. Optionally, you can explain your tool and how to use it in the instructions which can help the LLM make better tool calls.
---

## Tool Registry Usage

### Using the CLI
The CLI provides an interactive way to register tools.

1. Install the package:
```bash
pip install ncp-tool-registry-cli
```

2. Run the CLI command:
```bash
register-tool create-tool
```

3. Follow the interactive prompts:
   - Enter a tool ID (alphanumeric characters, underscores, and dashes only)
   - Provide tool information (title, description, version)
   - Enter the base URL of your API
   - Select an endpoint from the listed paths
   - Select HTTP methods to register
   - Optionally provide preprocessing and postprocessing JSONPath filters
   - Choose whether to sync the tool to Danswer

### Using the REST API
The API Gateway is available at `https://apigateway.vip.us-east-1.test.cloud.netflix.net`

#### Available Endpoints:
[FastAPI Docs with all endpoints](https://apigateway.vip.us-east-1.test.cloud.netflix.net/docs)

1. List all registered tools:
```http
GET /tool_registry
```

2. Register a new tool:
```http
POST /tool_registry/{tool_id}
```
Example:
```json
{
    "base_url": "https://your-api.netflix.net",
    "path": "/v1/endpoint",
    "methods": ["get", "post"],
    "info": {
        "title": "My Tool",
        "description": "Tool description",
        "version": "1.0"
    },
    "preprocessing_jsonpath": "$.data",
    "postprocessing_jsonpath": "$.result"
}
```

3. Get existing tool:
```http
GET /tool_registry/{tool_id}
```

4. Sync existing tool to Danswer:
```http
POST /tool_registry/{tool_id}/sync_to_danswer
```

### What Happens During Registration

1. **OpenAPI Discovery**: The system automatically discovers and parses the OpenAPI docs from the provided base URL to list possible endpoint paths and methods you can register.

2. **Schema Generation**: Request and response schemas are automatically generated based on the OpenAPI spec for the selected endpoint and methods.

3. **Stored Metadata**: The tool configuration is stored in ConfigBin with:
   - Tool info (title, description, version)
   - Request/response schemas
   - Invocation details (endpoint, app name)
   - Pre/postrocessing filters

4. **Danswer Sync**: If enabled, the tool is automatically added to Danswer, making it available for use in Chat2.

---

---

[![Open in Workspace](https://coder.prod.netflix.net/netflix/assets/open-ws-button.svg)](https://go.netflix.com/newdev?name=api-gateway&param.git_repo=https://github.netflix.net/corp/ncp-api-gateway)

## Install Dependencies

The dependencies of the project are defined in the `requirements.in` file.

The following command will create a virtual environment and install the
dependencies using the right python version specified in `.newt.yml`.

```bash
newt venv
```

Lock the dependencies by running: (see <https://go/python-deps/>)

```bash
newt deps lock
```

This will generate a `requirements.txt` file with all the transitive
dependencies locked to a version. Make sure you add it to your git repo:

```bash
git add requirements.txt tests/requirements.txt
git commit -m "Update lock files."
```

## Run Tests

```bash
newt tox
```

## Run Lint

```bash
newt tox -e style
```

To autofix lint errors, run

```bash
newt tox -e stylefix
```

## Pre-Commit Hooks

[pre-commit](https://pre-commit.com) is a tool for running checks on your code
before you commit it. This saves time by preventing you from making commits
that are likely to fail code review or break the build.

To install pre-commit hooks, run

```bash
newt cli install pre-commit   # Installs the pre-commit tool
pre-commit install    # Installs the pre-commit hooks
```

Now every time you commit, the pre-commit hooks will run. If any of the hooks
fail the commit will be aborted. Most of the failures can be fixed by running:

```bash
newt tox -e stylefix
```

## Run the Webapp

```bash
newt --app-type=mesh start -s root/etc/proxyd/input.yaml # start mesh server
.venv/bin/run-webapp # launch webapp
```

Visit <http://localhost:7101> or <https://localhost> to see the webapp.

## Local Docker Development

To emulate the production environment locally,

Build your docker image:

```bash
newt docker build --platform=linux/amd64
```

Run your docker image,

```bash
newt docker develop
```

Check the ports exposed by your docker image,

```bash
newt docker ps
```

Example output:

```bash
newt docker ps
CONTAINER ID   IMAGE                                 COMMAND            CREATED          STATUS          PORTS                                                                      NAMES
8a18d76c04ef   example/exampleflasktest:latest   "/nflx/bin/init"   37 minutes ago   Up 37 minutes   0.0.0.0:55006->443/tcp, 0.0.0.0:55005->7001/tcp, 0.0.0.0:55004->7004/tcp   example.exampleflasktest.docker_develop
```

You can access your webapp,  via a browser by visiting the host port that maps to the container port :443. In this example it is: <https://localhost:55006>. You have to use HTTPS protocol.

All webapp projects are configured to be secure by default.

The metatron enabled port is served via 7004. This is useful when accessing the service via `metatron curl`.

```bash
metatron curl -a exampleflasktest https://localhost:55004   # Note the host port that maps to the container port 7004.
```

## Nflxtrace Instrumentation

Available opentelemetry instrumentation of dependent libraries (including transitive dependencies) is validated when you
run `instrument_auto`, which can throw an exception telling you what to add to your requirements.  For example, if you
use `requests` it might say "You need to depend on `nflxtrace[requests]`" which means add the line `nflxtrace[requests]`
to your `requirements.txt`

If you want to check this manually, you can run `python -m nflxtrace.autotrace` from within the venv as well.

## Contributing Guideline

Open a Pull Request to contribute bug fixes or features.
Commit messages should contain concise and relevant information regarding the changes.
Pull Requests should be small, tidy and easy to review.
Tag the repository owner(s) for review before merging.

---

This project was seeded via `newt init --app-type python`, see [go/python](http://go/python) for more info.
