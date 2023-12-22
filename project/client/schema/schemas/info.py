import pydantic

class SchemaInfo(pydantic.BaseModel):
    name: str
    description: str
    version: str
    author: str
    license: str