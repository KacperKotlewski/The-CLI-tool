import typing
from pydantic import Field

from project.common.models.base import BaseModel
from ..abstract_handler import AbstractHandler

from .interface_class import Interface
    

class InterfaceHandler(AbstractHandler, BaseModel):
    """
    InterfaceHandler class is a class that handles interfaces.
    
    Args:
        items (List[Interface]): The interfaces of the handler.
    """
    items: typing.List[Interface] = list()
    items_instance: typing.Type = Field(default=Interface)
    
    def __init__(self, **data) -> None:
        super().__init__(**data)
        
    def __add__(self, other: typing.Union[Interface, typing.List[Interface], 'InterfaceHandler']) -> 'InterfaceHandler':
        return super().__add__(other)
    
    def __str__(self) -> str:
        return f"InterfaceHandler: \n\t" + "\t\n".join([str(interface) for interface in self.items])
    
    def __repr__(self) -> str:
        return f"InterfaceHandler: {self.items}"
    
    def filtered(self, condition: typing.Callable = None, type: typing.Type = None, required: bool = None) -> 'InterfaceHandler':
        return super().filtered(condition=condition, type=type, required=required)
    
    def execute(self, name: str, *args) -> typing.Any:
        return super().execute(name, *args)
    