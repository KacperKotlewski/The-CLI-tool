import typing
from pydantic import Field

from project.common.models.base import BaseModel
from ..abstract_handler import AbstractHandler

from .interface_class import Interface
from .user_interface_class import UserInterface
    

class InterfaceHandler(AbstractHandler, BaseModel):
    """
    InterfaceHandler class is a class that handles interfaces.
    
    Args:
        items (List[Interface]): The interfaces of the handler.
    """
    items: typing.List[Interface] = list()
    items_instance: typing.Type = Field(default=Interface)
    
    @property
    def active(self) -> Interface:
        """
        active gets the active interface.
        """
        return self._active
    
    @active.setter
    def active(self, value: Interface) -> None:
        """
        active sets the active interface.
        
        Args:
            value (Interface): The interface to set as active.
        """
        self._active = value
    
    def __init__(self, **data) -> None:
        super().__init__(**data)
        
    def add(self, item: typing.Union[Interface, typing.List[Interface], 'InterfaceHandler']) -> 'InterfaceHandler':
        items_count = len(self.items)
        super().add(item)
        if items_count == 0:
            self.active = self.items[0]
        return self
        
        
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
    
    def check_item_instance(self, item: typing.Any) -> bool:
        return True
    
    def set_active(self, name: str) -> None:
        """
        set_active sets the active interface.
        
        Args:
            name (str): The name of the interface to set as active.
        """
        interface = self.get(name)
        if interface:
            self.active = interface
        else:
            raise ValueError(f"Interface '{name}' does not exist.")