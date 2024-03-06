import typing
from .interface_class import Interface

class InterfaceNotImplementedError(Exception):
    pass

class UserInterface(Interface):
    """
    UserInterface class is the user interface class.
    
    """
    
    def __init__(self, **data) -> None:
        return super().__init__(**data)
    
    def prompt(self, message: str=None, required:bool=False, input_callback:typing.Optional[typing.Callable]=None, error_callback:typing.Optional[typing.Callable]=None) -> str:
        if input_callback is None or error_callback is None:
            raise InterfaceNotImplementedError("prompt method is not implemented")
        
        if message is None:
            message = "Enter value"
            
        while True:
            input_ = input_callback(message)
            if (input_ is not None) and ((not required) or (required and input_ != '')):
                return input_
            else:
                error_callback()
    
    def confirm(self, message: str) -> bool:
        raise InterfaceNotImplementedError("confirm method is not implemented")
    