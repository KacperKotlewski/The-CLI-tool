from abc import ABC, abstractmethod
import typing

from .command import Command
            
# decorator to create new command from function
def command_from_function(name: str, description: str, help_str: str, option_handler: 'OptionHandler' = None, action_handler: 'ActionHandler' = None) -> typing.Callable:
    def decorator(func: typing.Callable) -> Command:
        return Command(name=name, description=description, help_str=help_str, option_handler=option_handler, action_handler=action_handler, action=func)
    return decorator

T = typing.Union[typing.Callable]
# universal decorator to create new command
def command(name: str, description: str, help_str: str, option_handler: 'OptionHandler' = None, action_handler: 'ActionHandler' = None) -> typing.Callable:
    def decorator(element: T) -> Command:
        
        if isinstance(element, typing.Callable):
            comm = command_from_function(name, description, help_str, option_handler, action_handler)
            return comm(element)
        
        else:
            raise ValueError(f"Element '{element}' is not recognized.")
        
    return decorator