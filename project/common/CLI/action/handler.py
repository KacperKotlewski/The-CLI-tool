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
            