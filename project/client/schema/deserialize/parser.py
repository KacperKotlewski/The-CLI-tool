from .. import models
from . import exceptions as exc
from ..versions import Version
import typing
from .models import ParseData
    
def get_key_and_value(line:str) -> typing.Tuple[str, str]:
    key = line
    value = None
    
    if ":" in line:
        splited = line.split(":")
        if len(splited) != 2:
            raise exc.EnvSchemaParsingError(f"Cannot parse this line: {line}")
        else:
            key = splited[0].strip()
            value = splited[1].strip()
            
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
    if not isinstance(data.schema_model, models.Schema):
        raise exc.EnvSchemaParsingError()
    
    if data.line == "---":
        data.line_count+=1
        data.flag = True
        return data
    (key,value) = get_key_and_value(data.line)
    
    if key.lower() == "Author".lower() and versions.checkVersion(value):
        data.line_count+=1
        data.schema_model.schemaInfo.author = value
        return data
    
    raise exc.EnvSchemaParsingError(f"Cannot parse this line: {data.line}")
    

def parse_env_schema(schema_text:str) -> models.Schema:    
    schema:models.Schema = models.Schema()
    line_count = 0
    cli_info_flag, schema_info_flag = False
    for line in schema_text.split("\n"):
        line = line.strip()
        if line == "":
            continue
        if line.startswith("#"):
            line = line[1:].strip()
            if cli_info_flag == False:
                data = ParseData(
                    line=line,
                    line_count=line_count,
                    schema_model=schema,
                    flag=cli_info_flag
                )
                data = parse_cli_info(data)
                line = data.line
                line_count = data.line_count
                schema = data.schema_model
                cli_info_flag = data.flag
            elif schema_info_flag == False:
                data = ParseData(
                    line=line,
                    line_count=line_count,
                    schema_model=schema,
                    flag=schema_info_flag
                )
                data = parse_cli_info(data)
                line = data.line
                line_count = data.line_count
                schema = data.schema_model
                schema_info_flag = data.flag
                