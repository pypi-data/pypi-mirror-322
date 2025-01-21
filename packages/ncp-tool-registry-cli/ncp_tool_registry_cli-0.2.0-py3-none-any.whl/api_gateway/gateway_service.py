import logging

import jsonpath_ng
import requests
from metatron.http import MetatronAdapter
from fastapi import Request


from api_gateway.models.tool_models import ConfigBinTool

logger = logging.getLogger(__name__)


def replace_path_params(url, param_values):
    values = param_values.split("/")

    result = url
    value_index = 0
    start = 0

    while True:
        start = result.find("{", start)
        if start == -1 or value_index >= len(values):
            break

        end = result.find("}", start)
        if end == -1:
            break

        result = result[:start] + values[value_index] + result[end + 1 :]
        value_index += 1

    return result


def process_schema(schema, path_expression):
    try:
        jsonpath_expr = jsonpath_ng.parse(path_expression)
        matches = jsonpath_expr.find(schema)

        if not matches:
            return None

        if len(matches) == 1:
            return matches[0].value

        return [match.value for match in matches]
    except Exception:
        return None


async def invoke_tool(tool: ConfigBinTool, request: Request, additional_path: str = None) -> str:
    session = requests.Session()

    if tool.invocation.get("type") == "metatron_endpoint":
        session.mount("https://", MetatronAdapter(tool.invocation["app_name"]))
    url = tool.invocation["endpoint"]

    if additional_path:
        logger.info(f"Additional path: {additional_path}")
        url = replace_path_params(url, additional_path)

    try:
        body = await request.json()
    except Exception:
        body = None

    logger.info(f"Body: {body}")
    logger.info(f"Query params: {dict(request.query_params)}")

    headers = dict(request.headers)
    headers["Accept"] = "*/*"
    # hop_by_hop_headers = {
    #     "connection",
    #     "keep-alive",
    #     "proxy-authenticate",
    #     "proxy-authorization",
    #     "te",
    #     "trailers",
    #     "transfer-encoding",
    #     "upgrade",
    #     "host",
    # }
    # for header in hop_by_hop_headers:
    #     headers.pop(header.lower(), None)

    request_func = getattr(session, request.method.lower())
    logger.info(f"Sending {request.method} to: {url}")

    try:
        response = request_func(url, json=body, headers=headers, params=dict(request.query_params))
        response.raise_for_status()
        return response
    except requests.HTTPError as http_err:
        logger.error(f"HTTP error during invoke_metatron_tool: {http_err}")
        raise http_err
    except Exception as e:
        logger.error(f"Exception during invoke_metatron_tool: {e}")
        raise e
