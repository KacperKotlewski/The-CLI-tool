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
        
        data = baseData.model_copy(deep=True)
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
        
def test_parse_schema_info_invalid():
    """
    test_parse_schema_info_invalid test parsing of the schema info
    """
    datas = [
        (
            parser.ParseData(
                line="Author: author name/nickname",
                line_count=3,
                schema_model=models.SchemaInfo(),
                flag=True # invalid flag - flag is True should be False
            ), 
            exc.EnvSchemaParsingError
        ),
        (
            parser.ParseData(
                line="Author: author name/nickname",
                line_count=3,
                schema_model=models.Schema(), # invalid schema model - expected SchemaInfo
                flag=False
            ),
            exc.EnvSchemaInvalidModel
        ),
        (
            parser.ParseData(
                line="xyz: xyz", # invalid key
                line_count=3,
                schema_model=models.SchemaInfo(),
                flag=False 
            ),
            exc.EnvSchemaParsingError
        ),
        (
            parser.ParseData(
                line="xyz", # invalid line
                line_count=3,
                schema_model=models.SchemaInfo(),
                flag=False 
            ),
            exc.EnvSchemaParsingError
        ),
    ]
    
    for data, expected_exception in datas:
        catch = None
        try:
            parser.parse_schema_info(data)
        except Exception as e:
            catch = e
        finally:
            if expected_exception is None:
                if catch is not None:
                    assert False, f"Unexpected exception: {catch}"
            else:
                assert isinstance(catch, expected_exception), f"Unexpected exception: {catch} - expected: {expected_exception} - data: {data}"
                
def test_parse_schema_info_finish_valid():
    """
    test_parse_schema_info_finish_valid test parsing of the schema info
    """
    data = parser.ParseData(
        line = "---",
        line_count=4,
        schema_model=models.SchemaInfo(
            name="example",
            description="example schema",
            version="0.1",
            author="author name/nickname",
            license="MIT",
        ),
        flag=False 
    )
    data = parser.parse_schema_info(data)

    assert data.line_count == 5
    assert data.flag == True
    assert isinstance(data.schema_model, models.SchemaInfo)
    assert data.schema_model.isValid()
    
def test_parse_schema_info_finish_invalid():
    """
    test_parse_schema_info_finish_invalid test parsing of the schema info
    """
    finishing_line = "---"
    dataList = [
        parser.ParseData(
            line = finishing_line,
            line_count=4,
            schema_model=models.SchemaInfo(
                name="example",
                description="example schema",
                version="0.1",
                author="author name/nickname",
                license="MIT",
            ),
            flag=True # invalid flag - flag is True should be False
        ),
        parser.ParseData(
            line = finishing_line,
            line_count=3,
            schema_model=models.SchemaInfo(), # lack of required fields
            flag=False
        ),
    ]
    expected_exceptions = [exc.EnvSchemaParsingError, exc.EnvSchemaNotValid]
    for data, expected_exception in list(zip(dataList, expected_exceptions)):
        catch = None
        try:
            parser.parse_schema_info(data)
        except Exception as e:
            catch = e
        finally:
            if expected_exception is None:
                if catch is not None:
                    assert False, f"Unexpected exception: {catch}"
            else:
                assert isinstance(catch, expected_exception)
                
def test_parse_schema_text():
    """
    test_parse_schema_text test parsing of the schema text
    """
    lines = [
        "Header: example header",
        "Section: example section",
        "Subsection: example subsection",
        "Message: example message",
        "Space",
        "Divider",
    ]
    shuffle(lines)
    baseData = parser.ParseData(
        line="",
        line_count=5,
        schema_model=models.SchemaText()
    )
    
    for line in lines:
        key = line.split(":")[0].strip() if ":" in line else line.strip()
        value = line.split(":")[1].strip() if ":" in line else None
        
        data = baseData.model_copy(deep=True)
        data.line = line
        data = parser.parse_schema_text(data)
        
        assert data.line_count == 6
        assert isinstance(data.schema_model, models.SchemaText)
        if key == "Header":
            assert data.schema_model.type == models.SchemaTextTypes.header
            assert data.schema_model.text == value
        elif key == "Section":
            assert data.schema_model.type == models.SchemaTextTypes.section
            assert data.schema_model.text == value
        elif key == "Subsection":
            assert data.schema_model.type == models.SchemaTextTypes.subsection
            assert data.schema_model.text == value
        elif key == "Message":
            assert data.schema_model.type == models.SchemaTextTypes.message
            assert data.schema_model.text == value
        elif key == "Space":
            assert data.schema_model.type == models.SchemaTextTypes.space
            assert data.schema_model.text == None
        elif key == "Divider":
            assert data.schema_model.type == models.SchemaTextTypes.divider
            assert data.schema_model.text == None
        else:
            assert False, "Unexpected key"
        assert data.schema_model.isValidFiltered()
        
def test_parse_schema_text_invalid():
    """
    test_parse_schema_text_invalid test parsing of the schema text
    """
    datas = [
        (
            parser.ParseData(
                line="Header: example header",
                line_count=5,
                schema_model=models.Schema(), # invalid schema model - expected SchemaText
                flag=False
            ),
            exc.EnvSchemaInvalidModel
        ),
        (
            parser.ParseData(
                line="xyz: xyz", # invalid key
                line_count=5,
                schema_model=models.SchemaText()
            ),
            exc.EnvSchemaParsingError
        ),
        (
            parser.ParseData(
                line="xyz", # invalid line
                line_count=5,
                schema_model=models.SchemaText()
            ),
            exc.EnvSchemaParsingError
        ),
    ]
    
    for data, expected_exception in datas:
        catch = None
        try:
            parser.parse_schema_text(data)
        except Exception as e:
            catch = e
        finally:
            if expected_exception is None:
                if catch is not None:
                    assert False, f"Unexpected exception: {catch}"
            else:
                assert isinstance(catch, expected_exception), f"Unexpected exception: {catch} - expected: {expected_exception} - data: {data}"
                
def test_parse_schema_field():
    """
    test_parse_schema_field test parsing of the schema field
    """
    lines = [
        "Name: example_field",
        "Example: example value",
        "Description: example field",
        "Hint: example hint",
        "Type: string",
        "Regex: ^[a-z]+$",
        "Props: Required, Generate, Hidden",
        "Error: example error msg",
    ]
    shuffle(lines)
    baseData = parser.ParseData(
        line="",
        line_count=6,
        schema_model=models.SchemaField()
    )
    
    for line in lines:
        key = line.split(":")[0].strip() if ":" in line else line.strip()
        value = line.split(":")[1].strip() if ":" in line else None
        
        data = baseData.model_copy(deep=True)
        data.line = line
        data = parser.parse_field(data)
        
        assert data.line_count == 7
        assert isinstance(data.schema_model, models.SchemaField)
        if key == "Name":
            assert data.schema_model.name == value
        elif key == "Example":
            assert data.schema_model.example == value
        elif key == "Description":
            assert data.schema_model.description == value
        elif key == "Hint":
            assert data.schema_model.hint == value
        elif key == "Type":
            assert data.schema_model.type == value
        elif key == "Regex":
            assert data.schema_model.regex == value
        elif key == "Error":
            assert data.schema_model.error == value
        elif key == "Props":
            assert data.schema_model.props == [models.SchemaFieldProps.required, models.SchemaFieldProps.generate, models.SchemaFieldProps.hidden]
        else:
            assert False, f"Unexpected key: {key}"
        assert data.schema_model.isValidFiltered()       
        
def test_parse_schema_field_invalid():
    """
    test_parse_schema_field_invalid test parsing of the schema field
    """
    datas = [
        (
            parser.ParseData(
                line="Name: example_field",
                line_count=6,
                schema_model=models.Schema(), # invalid schema model - expected SchemaField
                flag=False
            ),
            exc.EnvSchemaInvalidModel
        ),
        (
            parser.ParseData(
                line="xyz: xyz", # invalid key
                line_count=6,
                schema_model=models.SchemaField()
            ),
            exc.EnvSchemaParsingError
        ),
        (
            parser.ParseData(
                line="xyz", # invalid line
                line_count=6,
                schema_model=models.SchemaField()
            ),
            exc.EnvSchemaParsingError
        ),
        (
            parser.ParseData(
                line="Regex: [", # invalid regex
                line_count=6,
                schema_model=models.SchemaField()
            ),
            exc.EnvSchemaParsingError
        ),
        (
            parser.ParseData(
                line="Props: Required, Generate, Hidden, Invalid", # invalid prop
                line_count=6,
                schema_model=models.SchemaField()
            ),
            exc.EnvSchemaParsingError
        ),
    ]
    
    for data, expected_exception in datas:
        catch = None
        try:
            parser.parse_field(data)
        except Exception as e:
            catch = e
        finally:
            if expected_exception is None:
                if catch is not None:
                    assert False, f"Unexpected exception: {catch}"
            else:
                assert isinstance(catch, expected_exception), f"Unexpected exception: {catch} - expected: {expected_exception} - data: {data}"         
                
def test_parse_env_schema_prefix():
    """
    test_parse_env_schema test parsing of the schema
    """
    schema_text = """
    # dotEnv schema
    # CliVersion: 0.1
    # ---
    """
    
    expected_schema = models.Schema(
        schematizerVersion=Version.v0_1,
        schemaInfo=models.SchemaInfo(),
    )
    
    schema = parser.parse_env_schema(schema_text)
    
    assert schema == expected_schema
    
    
def test_parse_env_schema_info():
    """
    test_parse_env_schema test parsing of the schema
    """
    schema_text = """
    # dotEnv schema
    # CliVersion: 0.1
    # ---
    # Author: author name/nickname
    # Description: example schema
    # License: MIT
    # Name: example
    # Version: 0.1
    # ---
    """
    
    expected_schema = models.Schema(
        schematizerVersion=Version.v0_1,
        schemaInfo=models.SchemaInfo(
            name="example",
            description="example schema",
            version="0.1",
            author="author name/nickname",
            license="MIT",
        )
    )
    
    schema = parser.parse_env_schema(schema_text)
    
    assert schema == expected_schema
    
def test_parse_env_schema_elements():
    """
    test_parse_env_schema test parsing of the schema
    """
    schema_text = """
    # dotEnv schema
    # CliVersion: 0.1
    # ---
    # Author: author name/nickname
    # Description: example schema
    # License: MIT
    # Name: example
    # Version: 0.1
    # ---
    
    # Header: example header
    # Section: example section
    # Subsection: example subsection
    # Message: example message
    # Space
    # Divider
    
    # Field:
    # - Name: example_field
    # - Example: example value
    # - Description: example field
    # - Hint: example hint
    # - Type: string
    # - Regex: ^[a-z]+$
    # - Props: Required, Generate, Hidden
    # - Error: example error msg
    FIELD_NAME=default_value
    """
    
    expected_schema = models.Schema(
        schematizerVersion=Version.v0_1,
        schemaInfo=models.SchemaInfo(
            name="example",
            description="example schema",
            version="0.1",
            author="author name/nickname",
            license="MIT",
        ),
        elements=[
            models.SchemaText(type=models.SchemaTextTypes.header, text="example header"),
            models.SchemaText(type=models.SchemaTextTypes.section, text="example section"),
            models.SchemaText(type=models.SchemaTextTypes.subsection, text="example subsection"),
            models.SchemaText(type=models.SchemaTextTypes.message, text="example message"),
            models.SchemaText(type=models.SchemaTextTypes.space),
            models.SchemaText(type=models.SchemaTextTypes.divider),
            models.SchemaField(
                name="FIELD_NAME",
                default="default_value",
                example="example value",
                description="example field",
                hint="example hint",
                type=models.SchemaFieldTypes.string,
                regex="^[a-z]+$",
                error="example error msg",
                props=[
                    models.SchemaFieldProps.required,
                    models.SchemaFieldProps.generate,
                    models.SchemaFieldProps.hidden,
                ]
            )
        ]
    )
    
    # assert parser.parse_env_schema(schema_text) == expected_schema