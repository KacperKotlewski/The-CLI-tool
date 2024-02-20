import typing

from pydantic import Field
from common.models.base import BaseModel
from common.CLI.option import OptionAbstract, Flag

from common.models.base import BaseModel
from common.CLI.abstract_handler import AbstractHandler

import typing

from .action import Action


class ActionHandler(AbstractHandler, BaseModel):
    """
    OptionsHandler class is a class that handles flags, arguments, and options.
    
    Args:
        items (List[OptionAbstract]): The flags, arguments, and options of the handler.
    """
    items: typing.List[Action] = list()
    items_instance: typing.Type = Field(default=Action)
        
    def _validate(self) -> None:
        super()._validate()
        self._validate_actions()
        
    def _validate_actions(self) -> None:
        for action in self.items:
            action._validate()
        # check for duplicate action names
        list_of_names = [action.name for action in self.items]
        if len(list_of_names) != len(set(list_of_names)):
            raise ValueError(f"ActionHandler has duplicate action names: \n{list_of_names}")
        
    def insert(self, index: int, action: Action) -> None:
        if action not in self.items:
            self.items.insert(index, action)
            self._validate_actions()
            
    def filtered(self, condition: typing.Callable = None) -> 'ActionHandler':
        return super().filtered(condition=condition)
    
        
    def execute(self, *args, **kwargs) -> int:
        count_of_executed_actions = 0
        
        for action in self.items:
            fetched = action.execute(*args, **kwargs)
            
            if fetched:
                count_of_executed_actions += 1
        return count_of_executed_actions
    
    def __len__(self) -> int:
        return super().__len__()
            

# class ActionHandler(BaseModel):
#     actions: typing.List[Action] = list()
    
#     def __init__(self, **data) -> None:
#         actions = data.get("actions", [])
        
#         super().__init__(**data)
#         self._validate()
        
#     def _validate(self) -> None:
#         self._validate_actions()
        
#     def _validate_actions(self) -> None:
#         for action in self.actions:
#             action._validate()
#         # check for duplicate action names
#         list_of_names = [action.name for action in self.actions]
#         if len(list_of_names) != len(set(list_of_names)):
#             raise ValueError(f"ActionHandler has duplicate action names: \n{list_of_names}")
        
#     def add_action(self, action: Action) -> None:
#         if action not in self.actions:
#             self.actions.append(action)
#             self._validate_actions()
            
#     def insert_action(self, index: int, action: Action) -> None:
#         if action not in self.actions:
#             self.actions.insert(index, action)
#             self._validate_actions()
            
#     def remove_action(self, action: Action) -> None:
#         if action in self.actions:
#             self.actions.remove(action)
            
#     def execute_actions(self, *args, **kwargs) -> int:
#         count_of_executed_actions = 0
        
#         for action in self.actions:
#             fetched = action.execute(*args, **kwargs)
            
#             if fetched:
#                 count_of_executed_actions += 1
#         return count_of_executed_actions
            
#     def get_action(self, action: Action) -> Action:
#         return action
    
#     def __add__(self, other: typing.Union[Action, typing.List[Action], 'ActionHandler']) -> 'ActionHandler':
#         if isinstance(other, Action):
#             self.add_action(other)
            
#         elif isinstance(other, list):
#             for action in other:
#                 self.add_action(action)
        
#         elif isinstance(other, ActionHandler):
#             self.__add__(other.actions)
            
#         return self