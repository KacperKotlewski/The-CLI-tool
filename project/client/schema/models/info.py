from common.models.base import BaseModel

class SchemaInfo(BaseModel):
    name: str = None
    description: str = None
    version: str = None
    author: str = None
    license: str = None