from common.models.base import BaseModel

class SchemaInfo(BaseModel):
    name: str = None
    description: str = None
    version: str = None
    author: str = None
    license: str = None
    
    def __str__(self) -> str:
        return f'''Schema Info:
Name: {self.name}
Description: {self.description}
Version: {self.version}
Author: {self.author}
License: {self.license}'''