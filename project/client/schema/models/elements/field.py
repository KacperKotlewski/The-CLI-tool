import enum
import typing
import pydantic
from common.models.base import BaseModel

class SchemaFieldTypes(enum.Enum):
    string = "string"
    integer = "int"
    boolean = "bool"
    float = "float"
    password = "password"
    uuid = "uuid"
    regex = "regex"
    base64 = "base64"
    
class SchemaFieldProps(enum.Enum):
    required = "Required"
    generate = "Generate"
    hidden = "Hidden"
    
def text_field_template(field: 'SchemaField') -> str:
    text =  '# Field:\n'
    if field.name:
        text += f'- Name:         {field.name}\n'
    if field.example:
        text += f'- Example:      {field.example}\n'
    if field.description:
        text += f'- Description:  {field.description}\n'
    if field.hint:
        text += f'- Hint:         {field.hint}\n'
    if field.type:
        text += f'- Type:         {field.type}\n'
    if field.regex:
        text += f'- Regex:        {field.regex}\n'
    if field.props:
        text += f'- Props:        {", ".join([prop.value for prop in field.props])}\n'
    if field.error:
        text += f'- Error:        {field.error}\n'
            
    text += f'{field.og_name}={field.default}\n'
    
    return text
    
class SchemaField(BaseModel):
    og_name: str = None
    default: typing.Optional[str] = None
    name: typing.Optional[str] = None
    example: typing.Optional[str] = None
    description: typing.Optional[str] = None
    hint: typing.Optional[str] = None
    type: SchemaFieldTypes = None
    regex: typing.Optional[str] = None
    props: typing.Optional[typing.List[SchemaFieldProps]] = None
    error: typing.Optional[str] = None
    
    # @pydantic.validator("props", pre=True)
    def _validate_props(cls, v):
        def validate_single_prop(prop):
            if prop not in SchemaFieldProps:
                raise ValueError(f"Invalid prop: {prop}")
            return prop
        
        if v is None:
            return []
        if isinstance(v, str):
            return [validate_single_prop(v)]
        if isinstance(v, list):
            return [validate_single_prop(prop) for prop in v]
        else:
            raise ValueError(f"Invalid props, expected list, got {type(v)} : \n{v}")
        
    def to_text(self) -> str:
        return text_field_template(self)