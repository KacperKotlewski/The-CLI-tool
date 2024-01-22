from .. import models
from . import exceptions as exc
from ..versions import Version
import typing
from .models import ParseData
import re
    
def get_key_and_value(line:str) -> typing.Tuple[str, str]:
    key = line
    value = None
    
    if ":" in line:
        splited = line.split(":")
        key = splited[0].strip()
        value = ":".join(splited[1:]).strip()
            
    return (key,value)

def parse_cli_config(data:ParseData) -> ParseData:
    if not isinstance(data.schema_model, models.Schema):
        raise exc.EnvSchemaParsingError()
    
    if data.line_count == 0:
        if data.line == "dotEnv schema":
            data.line_count+=1
            return data
        else:
            raise exc.EnvSchemaNotFound()
    if data.line == "---":
        if not data.schema_model.isValid():
            raise exc.EnvSchemaNotValid(schema=data.schema_model)
        if data.flag != False:
            raise exc.EnvSchemaParsingError()
        data.schema_model.schemaInfo = models.SchemaInfo()
        data.line_count+=1
        data.flag = True
        return data
        
    (key,value) = get_key_and_value(data.line)
    
    if key == "CliVersion" and Version.check(value):
        data.line_count+=1
        data.schema_model.schematizerVersion = Version.fetch(value)
        return data
    
    raise exc.EnvSchemaParsingError(f"Cannot parse this line: {data.line}")
        

def parse_schema_info(data:ParseData) -> ParseData:
    if not isinstance(data.schema_model, models.SchemaInfo):
        raise exc.EnvSchemaInvalidModel(model=data.schema_model)
    
    if data.flag != False:
        raise exc.EnvSchemaParsingError()
    
    if data.line == "---":
        if not data.schema_model.isValid():
            raise exc.EnvSchemaNotValid(schema=data.schema_model)
        data.line_count+=1
        data.flag = True
        return data
    (key,value) = get_key_and_value(data.line)
    
    if key.capitalize() == "Author":
        data.line_count+=1
        data.schema_model.author = value
        return data
    elif key.capitalize() == "Description":
        data.line_count+=1
        data.schema_model.description = value
        return data
    elif key.capitalize() == "License":
        data.line_count+=1
        data.schema_model.license = value
        return data
    elif key.capitalize() == "Name":
        data.line_count+=1
        data.schema_model.name = value
        return data
    elif key.capitalize() == "Version":
        data.line_count+=1
        data.schema_model.version = value
        return data
    
    raise exc.EnvSchemaParsingError(f"Cannot parse this line: {data.line}")

def parse_field(data:ParseData) -> ParseData:
    if not isinstance(data.schema_model, models.SchemaField):
        raise exc.EnvSchemaInvalidModel(model=data.schema_model)
    
    (key,value) = get_key_and_value(data.line)
    
    if key.capitalize() == "Name":
        data.line_count+=1
        data.schema_model.name = value
        return data
    elif key.capitalize() == "Description":
        data.line_count+=1
        data.schema_model.description = value
        return data
    elif key.capitalize() == "Type":
        try:
            for member in models.elements.field.SchemaFieldTypes:
                if member.value.capitalize() == value.capitalize():
                    data.schema_model.type = member
                    break
            if data.schema_model.type == None:
                raise exc.EnvSchemaParsingError(f"Cannot parse this line: {data.line} - Invalid type: {value}")
        except Exception as e:
            raise exc.EnvSchemaParsingError(f"Cannot parse this line: {data.line} - Invalid type: {value}")
        
        data.line_count+=1
        
        return data
    elif key.capitalize() == "Default":
        data.line_count+=1
        data.schema_model.default = value
        return data
    elif key.capitalize() == "Required":
        data.line_count+=1
        data.schema_model.required = value
        return data
    elif key.capitalize() == "Example":
        data.line_count+=1
        data.schema_model.example = value
        return data
    elif key.capitalize() == "Hint":
        data.line_count+=1
        data.schema_model.hint = value
        return data
    elif key.capitalize() == "Error":
        data.line_count+=1
        data.schema_model.error = value
        return data
    
    elif key.capitalize() == "Regex":
        assert True, f"Cannot parse this line: {data.line} - Invalid regex: {value}"
        
        try:
            re.compile(value)
            data.schema_model.regex = value
        except re.error:
            raise exc.EnvSchemaParsingError(f"Cannot parse this line: {data.line} - Invalid regex: {value}")
        
        data.line_count+=1
        return data
    
    elif key.capitalize() == "Props":
        data.line_count+=1
        values = value.split(",") if "," in value else [value]
        props = []
        for prop in values:
            prop = prop.strip()
            if prop.capitalize() in [member.value for member in models.elements.field.SchemaFieldProps]:
                prop = models.elements.field.SchemaFieldProps(prop.capitalize())
                props.append(prop)
            else:
                raise exc.EnvSchemaParsingError(f"Cannot parse this line: {data.line} - Invalid prop: {prop}")
        data.schema_model.props = props
        return data
    
    raise exc.EnvSchemaParsingError(f"Cannot parse this line: {data.line}")

def parse_schema_text(data:ParseData) -> ParseData:
    if not isinstance(data.schema_model, models.elements.text.SchemaText):
        raise exc.EnvSchemaInvalidModel(model=data.schema_model)
    
    (key,value) = get_key_and_value(data.line)
    key = key.capitalize()
    
    key_type = None
    for member in models.elements.text.SchemaTextTypes:
        if member.value == key.capitalize():
            key_type = member
            break
    if key_type == None:
        raise exc.EnvSchemaParsingError(f"Cannot parse this line: {data.line} - Invalid key type: {key}")
    
    data.schema_model.type = key_type
    if value != None:
        data.schema_model.text = value
        
    data.line_count+=1
    
    return data

def parse_schema_element(inputData:ParseData, element_in_developement:models.SchemaElement) -> (ParseData, models.SchemaElement):

    
    def finishField(line: str, inputData:ParseData, field_in_developement:models.SchemaField):
        og_name, default = line.split("=")
        field_in_developement.og_name = og_name.strip()
        field_in_developement.default = default.strip()
        inputData.schema_model.elements.append(field_in_developement)
        inputData.line_count+=1
        field_in_developement=None
        return inputData, field_in_developement
    
    if inputData.flag == True and element_in_developement != None and isinstance(element_in_developement, models.SchemaField):
        
        if inputData.line.startswith("#"):
            line = inputData.line[1:].strip()
            if line.startswith("-"):
                line = line[1:].strip()
                
            fieldData = ParseData(
                line=line,
                line_count=inputData.line_count,
                schema_model=element_in_developement,
                flag=inputData.flag
            )
            fieldData = parse_field(fieldData)
        
            inputData.line = fieldData.line
            inputData.line_count = fieldData.line_count
            element_in_developement = fieldData.schema_model
            inputData.flag = fieldData.flag
            
        else:
            out = finishField(inputData.line, inputData, element_in_developement)
            inputData.flag = False
            return out
            
    elif inputData.line.startswith("#"):
        line = inputData.line[1:].strip()
        key = line
        if ":" in line:
            key = line.split(":")[0].strip()
        
        if key.capitalize() == "Field":
            inputData.flag = True
            element_in_developement = models.SchemaField()
            inputData.line_count+=1
            
        elif key.capitalize() in [member.value for member in models.elements.text.SchemaTextTypes]:
            outputData = parse_schema_text(
                ParseData(
                    line=line,
                    line_count=inputData.line_count,
                    schema_model=models.elements.text.SchemaText()
            ))
            inputData.line = outputData.line
            inputData.line_count = outputData.line_count
            inputData.schema_model.elements.append(outputData.schema_model)
            
    elif "=" in inputData.line:
        element_in_developement = models.SchemaField()
        return finishField(inputData.line, inputData, element_in_developement)
        
    else:
        raise exc.EnvSchemaParsingError(f"Cannot parse this line: {inputData.line}")
    
    return inputData, element_in_developement
    

def parse_env_schema(schema_text:str) -> models.Schema:    
    schema:models.Schema = models.Schema()
    line_count = 0
    cli_info_flag = schema_info_flag = field_element_in_developement = False
    element_in_developement: typing.Optional[models.elements.SchemaElement] = None
    
    for line in schema_text.split("\n"):
        line = line.strip()
        if line == "":
            continue
        
        if cli_info_flag == False:
            data = ParseData(
                line=line[1:].strip(),
                line_count=line_count,
                schema_model=schema,
                flag=cli_info_flag
            )
            data = parse_cli_config(data)
            line = data.line
            line_count = data.line_count
            schema = data.schema_model
            cli_info_flag = data.flag
            continue
        
        if schema_info_flag == False:
            data = ParseData(
                line=line[1:].strip(),
                line_count=line_count,
                schema_model=schema.schemaInfo,
                flag=schema_info_flag
            )
            data = parse_schema_info(data)
            line = data.line
            line_count = data.line_count
            schema.schemaInfo = data.schema_model
            schema_info_flag = data.flag
            continue
        
        # process elements
        try:
            data, element_in_developement = parse_schema_element(
                ParseData(
                    line=line,
                    line_count=line_count,
                    schema_model=schema,
                    flag=field_element_in_developement
                ),
                element_in_developement
            )
            line = data.line
            line_count = data.line_count
            schema = data.schema_model
            field_element_in_developement = data.flag
            
        except Exception as e:
            if not isinstance(e, exc.EnvSchemaParsingError):
                raise e
            
    return schema
                