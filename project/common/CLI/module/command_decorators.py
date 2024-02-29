from inspect import isclass
import typing
from ..action.handler import ActionHandler

from ..option.options_handler import OptionHandler

from .command import Command
            
# decorator to create new command from function
def command_from_function(name: str, description: str, help_str: str, option_handler: 'OptionHandler', action_handler: 'ActionHandler') -> typing.Callable:
    def decorator(func: typing.Callable) -> Command:
        return Command(name=name, description=description, help_str=help_str, option_handler=option_handler, action_handler=action_handler, base_action=func)
    return decorator

def command_from_class(name: str, description: str, help_str: str, option_handler: 'OptionHandler', action_handler: 'ActionHandler') -> typing.Callable:
    def decorator(cls: typing.Type) -> Command:
        if issubclass(cls, Command):
            return cls(name=name, description=description, help_str=help_str, option_handler=option_handler, action_handler=action_handler, base_action=lambda *args, **kwargs: (print(f"Command '{name}' is not implemented. \nTry to implement 'command' method in class '{cls.__name__}'.")))
        else:
            raise ValueError(f"Element '{cls}' is not recognized.")
    return decorator

T = typing.Union[typing.Callable, typing.Type]
# universal decorator to create new command
def command(name: str, description: str, help_str: str, option_handler: 'OptionHandler' = None, action_handler: 'ActionHandler' = None) -> typing.Callable:
    if option_handler is None:
        option_handler = OptionHandler()
    if action_handler is None:
        action_handler = ActionHandler()
        
    def decorator(element: T) -> Command:        
        if isclass(element):
            comm = command_from_class(name=name, description=description, help_str=help_str, option_handler=option_handler, action_handler=action_handler)
            return comm(element)
        
        if isinstance(element, typing.Callable):
            comm = command_from_function(name=name, description=description, help_str=help_str, option_handler=option_handler, action_handler=action_handler)
            return comm(element)
        
        else:
            raise ValueError(f"Element '{element}' is not recognized.")
        
    return decorator