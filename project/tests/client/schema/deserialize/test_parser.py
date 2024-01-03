import pytest
from client.schema.deserialize import parser, exceptions as exc
from client.schema import models
from client.schema.versions import Version
from random import shuffle

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
    
def test_parse_cli_config_second_line_valid():
    """
    test_parse_cli_config_2 test checking of the second line of the schema file containing "CliVersion"
    """
    versions = {
        "0.1": Version.v0_1,
        "0.1.1": Version.v0_1_1,
        "0.1.x": Version.v0_1_1,
        "0.x": Version.v0_1_1,
        "1.0": exc.EnvSchemaParsingError,
    }
    for version, expected in versions.items():
        data = parser.ParseData(
            line=f"CliVersion: {version}",
            line_count=1,
            schema_model=models.Schema(),
            flag=None
        )
        try:
            data = parser.parse_cli_config(data)
            assert data.line_count == 2
            assert data.flag == None
            assert isinstance(data.schema_model, models.Schema)
            assert data.schema_model.schematizerVersion == expected
        except Exception as e:
            assert expected == e.__class__    
            
def test_cli_config_finish_valid():
    """
    test_cli_config_finish testing finishing flag in the cli config
    """
    data = parser.ParseData(
        line = "---",
        line_count=2,
        schema_model=models.Schema(schematizerVersion=Version.v0_1),
        flag=False 
    )
    data = parser.parse_cli_config(data)

    assert data.line_count == 3
    assert data.flag == True
    assert isinstance(data.schema_model, models.Schema)
    assert data.schema_model.schematizerVersion == Version.v0_1
    assert data.schema_model.isValidFiltered()
    
def test_cli_config_finish_invalid():
    """
    test_cli_config_finish testing finishing flag in the cli config
    """
    finishing_line = "---"
    dataList = [
        parser.ParseData(
            line = finishing_line,
            line_count=2,
            schema_model=models.Schema(schematizerVersion=Version.v0_1),
            flag=True # invalid flag - flag is True should be False
        ),
        parser.ParseData(
            line = finishing_line,
            line_count=1,
            schema_model=models.Schema(), # invalid schema model - schematizerVersion is None
            flag=False 
        ),
        parser.ParseData(
            line = finishing_line,
            line_count=0, # invalid line count - should be 2
            schema_model=models.Schema(schematizerVersion=Version.v0_1),
            flag=False 
        ),
    ]
    expected_exceptions = [exc.EnvSchemaParsingError, exc.EnvSchemaNotValid, exc.EnvSchemaNotFound]
    for data, expected_exception in list(zip(dataList, expected_exceptions)):
        catch = None
        try:
            parser.parse_cli_config(data)
        except Exception as e:
            catch = e
        finally:
            if expected_exception is None:
                if catch is not None:
                    assert False, f"Unexpected exception: {catch}"
            else:
                assert isinstance(catch, expected_exception)
                
def test_parse_schema_info():
    """
    test_parse_schema_info test parsing of the schema info
    """
    lines = [
        "Author: author name/nickname",
        "Description: example schema",
        "License: MIT",
        "Name: example",
        "Version: 0.1",
    ]
    shuffle(lines)
    baseData = parser.ParseData(
        line="",
        line_count=3,
        schema_model=models.SchemaInfo(),
        flag=False 
    )
    
    for line in lines:
        key = line.split(":")[0].strip()
        value = line.split(":")[1].strip()
        
        data = baseData.model_copy()
        data.line = line
        data = parser.parse_schema_info(data)
        
        assert data.line_count == 4
        assert data.flag == False
        assert isinstance(data.schema_model, models.SchemaInfo)
        if key == "Author":
            assert data.schema_model.author == value
        elif key == "Description":
            assert data.schema_model.description == value
        elif key == "License":
            assert data.schema_model.license == value
        elif key == "Name":
            assert data.schema_model.name == value
        elif key == "Version":
            assert data.schema_model.version == value
        else:
            assert False, "Unexpected key"
        assert data.schema_model.isValidFiltered()