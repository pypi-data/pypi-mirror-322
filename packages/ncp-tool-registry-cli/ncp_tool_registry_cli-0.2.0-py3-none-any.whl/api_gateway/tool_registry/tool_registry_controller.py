from fastapi import APIRouter, Query, HTTPException, Request
from typing import Dict

from api_gateway.gandalf_helper import is_authorized, PermissionLevel
from api_gateway.tool_registry.tool_registry_operations import ToolRegistryOperations
from api_gateway.models.tool_models import RegistryTool, CreateToolRequest, ConfigBinToolConfig, UpdateToolRequest, ReconfigureToolRequest

router = APIRouter(tags=["Tool Registry"])
tool_ops = ToolRegistryOperations()


@router.get("/tool_registry", response_model=Dict[str, ConfigBinToolConfig])
async def list_tools() -> Dict[str, ConfigBinToolConfig]:
    tool_ops.sync_registry()
    try:
        return tool_ops.list_tools()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/tool_registry/{tool_id}", response_model=RegistryTool)
async def register_tool(
    tool_id: str,
    body: CreateToolRequest,
    sync_to_danswer: bool = Query(True, description="Flag to sync the tool to Danswer after registration"),
) -> RegistryTool:
    tool_ops.sync_registry()
    try:
        return tool_ops.register_tool(tool_id, body, sync_to_danswer)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to register tool: {e}")


@router.get("/tool_registry/{tool_id}", response_model=RegistryTool)
async def get_tool(tool_id: str) -> RegistryTool:
    tool_ops.sync_registry()
    tool = tool_ops.get_tool(tool_id)
    if tool is None:
        tool_ops.sync_registry()
        tool = tool_ops.get_tool(tool_id)
        if tool is None:
            raise HTTPException(status_code=404, detail="Tool not found")
    return tool


@router.delete("/tool_registry/{tool_id}")
async def delete_tool(tool_id: str, request: Request) -> str:
    tool_ops.sync_registry()
    if not is_authorized(request, tool_ops.get_tool(tool_id).permissions, PermissionLevel.OWNER):
        raise HTTPException(
            status_code=403,
            detail=f"Unauthorized: only users with access to the owner NCP project {tool_ops.get_tool(tool_id).permissions.owner.project_id} can delete this tool.",
        )
    try:
        return tool_ops.delete_tool(tool_id)
    except ValueError:
        tool_ops.sync_registry()
        try:
            return tool_ops.delete_tool(tool_id)
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/tool_registry/{tool_id}", response_model=RegistryTool)
async def update_tool(tool_id: str, request: Request, body: UpdateToolRequest) -> RegistryTool:
    tool_ops.sync_registry()
    if not is_authorized(request, tool_ops.get_tool(tool_id).permissions, PermissionLevel.OWNER):
        raise HTTPException(
            status_code=403,
            detail=f"Unauthorized: only users with access to the owner NCP project {tool_ops.get_tool(tool_id).permissions.owner.project_id} can update this tool.",
        )
    try:
        return tool_ops.update_tool(tool_id, body)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/tool_registry/{tool_id}", response_model=RegistryTool)
async def reconfigure_tool(tool_id: str, request: Request, body: ReconfigureToolRequest) -> RegistryTool:
    tool_ops.sync_registry()
    if not is_authorized(request, tool_ops.get_tool(tool_id).permissions, PermissionLevel.OWNER):
        raise HTTPException(
            status_code=403,
            detail=f"Unauthorized: only users with access to the owner NCP project {tool_ops.get_tool(tool_id).permissions.owner.project_id} can reconfigure this tool.",
        )
    try:
        return tool_ops.reconfigure_tool(tool_id, body)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/tool_registry/{tool_id}/sync_to_danswer")
async def sync_tool_to_danswer(tool_id: str, request: Request) -> str:
    tool_ops.sync_registry()
    if not is_authorized(request, tool_ops.get_tool(tool_id).permissions, PermissionLevel.OWNER):
        raise HTTPException(
            status_code=403,
            detail=f"Unauthorized: only users with access to the owner NCP project {tool_ops.get_tool(tool_id).permissions.owner.project_id} can sync this tool to Danswer.",
        )
    try:
        return tool_ops.sync_tool_to_danswer(tool_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/graphql")
async def graphql(base_url: str):
    try:
        schema = tool_ops.fetch_graphql_schema(base_url)
        if schema is None:
            raise HTTPException(status_code=400, detail="Failed to fetch GraphQL schema")
        return schema
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
