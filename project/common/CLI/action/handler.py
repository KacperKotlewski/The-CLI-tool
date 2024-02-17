import typing
from common.models.base import BaseModel
from common.CLI.option import OptionAbstract, Flag

from .action import Action

class ActionHandler(BaseModel):
    actions: typing.List[Action] = list()
    
    def __init__(self, **data) -> None:
        super().__init__(**data)
        self._validate()
        
    def _validate(self) -> None:
        self._validate_actions()
        
    def _validate_actions(self) -> None:
        for action in self.actions:
            action._validate()
        # check for duplicate action names
        list_of_names = [action.name for action in self.actions]
        if len(list_of_names) != len(set(list_of_names)):
            raise ValueError(f"ActionHandler has duplicate action names: \n{list_of_names}")
        
    def add_action(self, action: Action) -> None:
        if action not in self.actions:
            self.actions.append(action)
            self._validate_actions()
            
    def remove_action(self, action: Action) -> None:
        if action in self.actions:
            self.actions.remove(action)
            
    def execute_actions(self, *args, **kwargs) -> int:
        count_of_executed_actions = 0
        
        for action in self.actions:
            fetched = action.execute(*args, **kwargs)
            
            if fetched:
                count_of_executed_actions += 1
        return count_of_executed_actions
            
    def get_action(self, action: Action) -> Action:
        return action
    
    def __add__(self, other: typing.Union[Action, typing.List[Action], 'ActionHandler']) -> 'ActionHandler':
        if isinstance(other, Action):
            self.add_action(other)
            
        elif isinstance(other, list):
            for action in other:
                self.add_action(action)
        
        elif isinstance(other, ActionHandler):
            self.__add__(other.actions)
            
        return self