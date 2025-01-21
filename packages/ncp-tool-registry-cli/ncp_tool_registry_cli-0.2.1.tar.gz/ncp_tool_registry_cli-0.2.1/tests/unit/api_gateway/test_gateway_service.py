from src.api_gateway.gateway_service import replace_path_params, process_schema


def test_replace_single_param():
    url = "https://api.example.com/v1/{param1}/test"
    param_values = "value1"
    result = replace_path_params(url, param_values)
    assert result == "https://api.example.com/v1/value1/test"


def test_replace_multiple_params():
    url = "https://api.example.com/v1/{param1}/{param2}/test"
    param_values = "value1/value2"
    result = replace_path_params(url, param_values)
    assert result == "https://api.example.com/v1/value1/value2/test"


def test_no_params():
    url = "https://api.example.com/v1/test"
    param_values = "value1"
    result = replace_path_params(url, param_values)
    assert result == "https://api.example.com/v1/test"


def test_jsonpath():
    schema = {"data": {"value": "test"}}
    result = process_schema(schema, "$.data.value")
    assert result == "test"


def test_array_jsonpath():
    schema = {"data": {"items": [{"id": 1}, {"id": 2}]}}
    result = process_schema(schema, "$.data.items[*].id")
    assert result == [1, 2]


def test_single_dict_result():
    schema = {"data": {"item": {"id": 1, "name": "test"}}}
    result = process_schema(schema, "$.data.item")
    assert result == {"id": 1, "name": "test"}


def test_invalid_jsonpath():
    schema = {"data": {"value": "test"}}
    result = process_schema(schema, "invalid.path")
    assert result is None


def test_no_matches():
    schema = {"data": {"value": "test"}}
    result = process_schema(schema, "$.nonexistent")
    assert result is None
