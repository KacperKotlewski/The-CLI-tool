from . import exceptions as exc
import typing
    
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
