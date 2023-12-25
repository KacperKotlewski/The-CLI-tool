import pytest
from client.schema.deserialize import parser, exceptions as exc
from client.schema import models
from client.schema.versions import Version

def test_get_key_and_value():
    lines = {
        "some_key : some_value": ("some_key", "some_value"),
        "key_int : 123": ("key_int", "123"),
        "key_list1 : x,y,z": ("key_list1", "x,y,z"),
        "key_list2 : [x,y,z]": ("key_list2", "[x,y,z]"),
        "empty": ("empty", None),
        "error: : error": exc.EnvSchemaParsingError,
    }
    
    for line, expected in lines.items():
        try:
            (key,value) = parser.get_key_and_value(line)
            assert key == expected[0]        
            assert value == expected[1]
        except Exception as e:
            assert isinstance(e, expected)
    
def test_parse_cli_config_first_line_valid():
    """
    test_parse_cli_config_1 test checking of the first line of the schema file containing "dotEnv schema"
    """
    data = parser.ParseData(
        line="dotEnv schema",
        line_count=0,
        schema_model=models.Schema(),
        flag=None
    )
    data = parser.parse_cli_config(data)
    
    assert data.line_count == 1
    assert data.flag == None
    assert isinstance(data.schema_model, models.Schema)
    assert data.schema_model.schematizerVersion == None
    
def test_parse_cli_config_first_line_invalid():
    """
    test_parse_cli_config_1 test checking of the first line of the schema file containing "dotEnv schema"
    """
    data = parser.ParseData(
        line="dotEnv x schema",
        line_count=0,
        schema_model=models.Schema(),
        flag=None
    )
    try:
        parser.parse_cli_config(data)
    except exc.EnvSchemaNotFound:
        assert True
    else:
        assert False, "EnvSchemaNotFound exception not raised"
