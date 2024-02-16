import enum
import random
import re
import string
import typing
import uuid
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
    
class GeneratorField(BaseModel):
    min_value: typing.Optional[typing.Union[int, float]] = None
    max_value: typing.Optional[typing.Union[int, float]] = None
    min_length: typing.Optional[int] = None
    max_length: typing.Optional[int] = None
    length: typing.Optional[int] = None
    
    def generate(self, type: SchemaFieldTypes) -> str:
        if type in [SchemaFieldTypes.string, SchemaFieldTypes.password, SchemaFieldTypes.base64]:
            special_chars = ''.join(set(string.punctuation) - {'#', '='})
            return ''.join(random.choices(string.ascii_letters + string.digits + special_chars, k=self.length))
                
        elif type == SchemaFieldTypes.integer:
            min_value = self.min_value if self.min_value is not None else -2**31
            max_value = self.max_value if self.max_value is not None else 2**31 - 1
            return str(random.randint(min_value, max_value))
        
        elif type == SchemaFieldTypes.float:
            min_value = self.min_value if self.min_value is not None else -3.4e38
            max_value = self.max_value if self.max_value is not None else 3.4e38
            return str(random.uniform(min_value, max_value))
        
        elif type == SchemaFieldTypes.uuid:
            return str(uuid.uuid4())
        
        else:
            raise ValueError(f"Invalid type: {type}")
    
    
def text_field_template(field: 'SchemaField') -> str:
    text =  '# Field:\n'
    if field.name:
        text += f'# - Name:         {field.name}\n'
    if field.example:
        text += f'# - Example:      {field.example}\n'
    if field.description:
        text += f'# - Description:  {field.description}\n'
    if field.hint:
        text += f'# - Hint:         {field.hint}\n'
    if field.type:
        text += f'# - Type:         {field.type}\n'
    if field.regex:
        text += f'# - Regex:        {field.regex}\n'
    if field.props:
        text += f'# - Props:        {", ".join([prop.value for prop in field.props])}\n'
    if field.error:
        text += f'# - Error:        {field.error}\n'
            
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
    # generator: typing.Optional[GeneratorField] = None
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
    
    def introduce(self) -> str:
        return f"Field: {self.og_name}"
    
    def check_regex(self, value: str) -> bool:
        if self.regex is not None:
            return bool(re.match(self.regex, value))
        else:
            return True
    
    def generate(self) -> str:
        # if self.generator is None:
        #     raise ValueError(f"Field {self.og_name} has no generate field")
        # while True:
        #     value = self.generator.generate(self.type)
        #     if self.check_regex(value):
        #         return value
        if self.props is None or SchemaFieldProps.generate not in self.props:
            raise ValueError(f"Field {self.og_name} has no generate field")
        while True:
            value = GeneratorField(length=32).generate(self.type)
            if self.check_regex(value):
                return value
        
    def is_hidden(self) -> bool:
        if self.props is None:
            return False
        return SchemaFieldProps.hidden in self.props
    
    def is_required(self) -> bool:
        if self.props is None:
            return False
        return SchemaFieldProps.required in self.props
    
    def is_generated(self) -> bool:
        return self.generator is not None