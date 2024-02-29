import typing
from common.CLI.option import OptionAbstract, Flag

from .action import Action
from .builder import ActionBuilder

class ActionFactory:
    @staticmethod
    def action_builder(name: str, function: typing.Callable, condition: typing.Callable) -> ActionBuilder:
        builder = ActionBuilder()
        
        if not name or not isinstance(name, str):
            raise ValueError(f"Action name is not a string: {name}")
        builder.set_name(name)
        
        if not function or not callable(function):
            raise ValueError(f"Action function is not callable: {function}")
        builder.set_function(function)
        
        if not condition or not callable(condition):
            raise ValueError(f"Action condition is not callable: {condition}")
        builder.set_condition(condition)
        
        return builder
    
    @staticmethod
    def action(name: str, function: typing.Callable, condition: typing.Callable) -> Action:
        builder = ActionFactory.action_builder(name, function, condition)
        return builder.build()
    
    @staticmethod
    def from_flag(option: 'Flag', function: typing.Callable) -> Action:
        if not isinstance(option, Flag):
            raise ValueError(f"Option is not a Flag: {option}")
        
        condition = lambda *args: option.is_set()
        return ActionFactory.action(option.name, function, condition)
    
    @staticmethod
    def from_option(option: OptionAbstract, condition: typing.Callable, function: typing.Callable) -> Action:
        return ActionFactory.action(option.name, function, condition)