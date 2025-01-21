import logging
from typing import Any, Dict

from nflxconfig import NXCONF
import requests
import uvicorn
from fastapi import FastAPI, HTTPException, Request, Body
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from nflx_security_util import get_authorized_caller
from nflx_security_util.utils import NflxSecurityUtilException
import nflxlog
import nflxtrace
from nflxlog.nflxlogger import NflxLogger
from contextlib import asynccontextmanager
from spectator import GlobalRegistry
from nflxmetrics.fastapi_middleware import MetricsMiddleware
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware

from api_gateway.gandalf_helper import is_authorized, PermissionLevel
from api_gateway.gateway_service import invoke_tool, process_schema
from api_gateway.tool_registry.tool_managers.configbin import ConfigbinManager
from api_gateway.tool_registry.tool_registry_controller import router as tool_registry_router


NXCONF.defaults.load_config(__file__)
logger = NflxLogger(__name__)

logging.getLogger("urllib3.connectionpool").setLevel(logging.DEBUG)
nflxlog.init()
nflxtrace.trace_init()
nflxtrace.instrument_auto()
logging.getLogger().setLevel(logging.DEBUG)


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        app.configbin_manager = ConfigbinManager()
        logger.info("Successfully loaded tools from ConfigBin")

    except Exception as e:
        logger.error(f"Failed to initialize ConfigBin: {e}")
        raise

    yield

    app.configbin_manager = None


APP = FastAPI(lifespan=lifespan)

APP.add_middleware(SentryAsgiMiddleware)
APP.add_middleware(MetricsMiddleware)

APP.include_router(tool_registry_router)

nflxtrace.instrument_fastapi_app(APP)


@APP.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.error(f"Validation error: {exc.errors()}")
    return JSONResponse(status_code=422, content={"detail": exc.errors()})


@APP.api_route(
    "/ncp_model_gateway/v1/function/{tool_id}/invoke",
    methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
    operation_id="gateway_invoke",
    tags=["API Gateway"],
)
@APP.api_route(
    "/ncp_model_gateway/v1/function/{tool_id}/invoke/{path:path}",
    methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
    operation_id="gateway_invoke_with_path",
    tags=["API Gateway"],
)
async def gateway(tool_id: str, request: Request, body: Dict[str, Any] = Body(default=None), path: str = None):
    APP.configbin_manager.sync_tool_registry()
    tool = APP.configbin_manager.get_tool_by_id(tool_id)
    if not tool:
        APP.configbin_manager.sync_tool_registry()
        tool = APP.configbin_manager.get_tool_by_id(tool_id)
        if not tool:
            tool_not_found_message = f"ERROR! Tool not found: {tool_id}"
            logger.error(tool_not_found_message)
            GlobalRegistry.counter("tool_invocation_count", tags={"tool_id": tool_id}).increment()
            raise HTTPException(status_code=404, detail=tool_not_found_message)

    logger.info(f"Checking authorization for tool {tool_id}")
    if not is_authorized(request, tool.permissions, PermissionLevel.BASIC):
        unauthorized_message = f"ERROR! Unauthorized to call tool: {tool_id}"
        logger.error(unauthorized_message)
        raise HTTPException(status_code=403, detail=unauthorized_message)

    logger.info(f"Calling tool: {tool.tool_id}")
    GlobalRegistry.counter("tool_invocation_count", tags={"tool_id": tool_id}).increment()
    
    try:
        response = await invoke_tool(tool, request, additional_path=path)

        if response is None:
            logger.info("Response: None received from tool")

            # We still want to let the LLM know the tool was successfully called even if there is no response
            return f"Success! Done calling tool: {tool_id}"

        if tool.postprocessing_jsonpath:
            try:
                json_data = response.json()
                filtered = process_schema(json_data, tool.postprocessing_jsonpath)
                logger.info("Applied postprocessing: original length %s, filtered length %s", len(str(json_data)), len(str(filtered)))
                return filtered
            except ValueError as e:
                logger.warning(f"Postprocessing failed: response wasn't valid JSON: {e}")

        if response.text:
            try:
                json_data = response.json()
                logger.info(f"JSON Response: {str(json_data)[:500]}")
                return json_data
            except ValueError:
                logger.info(f"Text Response: {response.text[:500]}")
                return response.text

        # We still want to let the LLM know the tool was successfully called even if there is no response
        return f"Success! Done calling tool: {tool_id}"

    except requests.HTTPError as http_error:
        error_message = f"ERROR! Failed to call tool with HTTPException: {http_error}"
        logger.error(error_message)
        raise HTTPException(status_code=400, detail=error_message)
    except Exception as e:
        error_message = f"ERROR! Failed to call tool with exception: {e}"
        logger.error(error_message)
        raise HTTPException(status_code=500, detail=error_message)


@APP.get("/protected", tags=["API Gateway"])
async def protected(request: Request) -> str:
    """
    Example on how to use nflx-security-util
    for authZ.
    """
    try:
        caller = get_authorized_caller(request)  # extract information about direct/initial caller identity
    except NflxSecurityUtilException as e:
        raise HTTPException(status_code=403, detail=str(e))

    # example for matching direct caller identity type
    if caller.direct.identityType == "User":
        return f"Email: {caller.direct.identity.username}"
        # even more details about a User can be extracted with caller.direct.identity.get_user_details()
    elif caller.direct.identityType == "Application":
        return f"Application Name: {caller.direct.identity.applicationName}"
    else:
        return f"Identity: {caller.direct.identityType}"


@APP.get("/healthcheck", tags=["API Gateway"])
async def healthcheck() -> str:
    GlobalRegistry.counter("healthcheck").increment()
    return "OK"


if __name__ == "__main__":
    logger.configure()
    port = NXCONF.get_int("server.port", 7101)
    logger.info(f"Starting server on port {port}")
    uvicorn.run("api_gateway.webapp:APP", host="0.0.0.0", port=port, log_level="info", reload=True)
