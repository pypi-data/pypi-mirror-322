import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch, MagicMock

from src.api_gateway.webapp import APP
from src.api_gateway.models.tool_models import ConfigBinTool, Info, Permissions, GenAIProject

from nflx_security_util.testing import AppCallerTestClient, UserCallerTestClient


@pytest.fixture
def mock_tool():
    return ConfigBinTool(
        tool_id="test-tool",
        permissions=Permissions(
            owner=GenAIProject(env="test", project_id="test", gandalf_policy="test"),
            accessibility="public",
            allowed_projects=[],
        ),
        response_schema={},
        openapi="3.1.0",
        info=Info(title="Test Tool", description="Test Description", version="1.0.0"),
        request_schema={},
        invocation={"endpoint": "https://api.example.com/v1/test", "type": "hi"},
        components={},
    )


@pytest.fixture
def mock_configbin_manager(mock_tool):
    manager = MagicMock()
    manager.get_tool_by_id = Mock(side_effect=lambda x: mock_tool if x == "test-tool" else None)
    return manager


@pytest.fixture
def test_client(mock_configbin_manager):
    APP.configbin_manager = mock_configbin_manager
    client = TestClient(APP)
    yield client
    APP.configbin_manager = None


def test_tool_not_found(test_client):
    response = test_client.post("/ncp_model_gateway/v1/function/nonexistent/invoke")
    assert response.status_code == 404
    assert "Tool not found" in response.json()["detail"]


def test_successful_invocation_json(test_client):
    with patch("src.api_gateway.webapp.invoke_tool") as mock_invoke:
        mock_response = Mock()
        mock_response.json.return_value = "Success"
        mock_invoke.return_value = mock_response

        response = test_client.post("/ncp_model_gateway/v1/function/test-tool/invoke")

        assert response.status_code == 200
        mock_invoke.assert_called_once()


def test_successful_invocation_text(test_client):
    with patch("src.api_gateway.webapp.invoke_tool") as mock_invoke:
        mock_response = Mock()
        mock_response.text = "Success"
        mock_response.json.side_effect = ValueError("Not JSON")  # Force JSON parsing to fail
        mock_invoke.return_value = mock_response

        response = test_client.post("/ncp_model_gateway/v1/function/test-tool/invoke")

        assert response.status_code == 200
        mock_invoke.assert_called_once()
        assert response.json() == "Success"


def test_invocation_with_path(test_client):
    with patch("src.api_gateway.webapp.invoke_tool") as mock_invoke:
        mock_response = Mock()
        mock_response.json.return_value = {"key": "value"}
        mock_invoke.return_value = mock_response

        response = test_client.post("/ncp_model_gateway/v1/function/test-tool/invoke/additional/path")

        assert response.status_code == 200
        mock_invoke.assert_called_once()
        assert mock_invoke.call_args[1]["additional_path"] == "additional/path"


def test_postprocessing(test_client, mock_tool):
    mock_tool.postprocessing_jsonpath = "$.data"
    with patch("src.api_gateway.webapp.invoke_tool") as mock_invoke:
        mock_response = Mock()
        mock_response.text = "Success"
        mock_response.json.return_value = {"data": {"key": "value"}}
        mock_invoke.return_value = mock_response

        response = test_client.post("/ncp_model_gateway/v1/function/test-tool/invoke")

        assert response.status_code == 200
        mock_invoke.assert_called_once()
        assert response.json() == {"key": "value"}


def test_protected():
    user_test_client = UserCallerTestClient(APP, username="test@netflix.com")
    rv = user_test_client.get("/protected")
    assert rv.status_code == 200
    assert rv.json() == "Email: test@netflix.com"

    app_test_client = AppCallerTestClient(APP, applicationName="testapp")
    rv = app_test_client.get("/protected")
    assert rv.status_code == 200
    assert rv.json() == "Application Name: testapp"


def test_healthcheck(test_client):
    rv = test_client.get("/healthcheck")
    assert rv.status_code == 200
    assert rv.headers["content-type"] == "application/json"
    assert rv.json() == "OK"
