import typing
from inspect import isclass

from .interface_class import Interface
from .user_interface_class import UserInterface


T = typing.Union[Interface, UserInterface]
# universal decorator to create new command
def interface(name: str, description: str) -> typing.Callable:
    def decorator(element: T) -> Interface:
        
        interface = None
        
        if issubclass(element, UserInterface):
            interface = element(name=name, description=description)
        
        if interface is not None:
            return interface        
        else:
            raise ValueError(f"Element '{element}' is not recognized.")
        
    return decorator