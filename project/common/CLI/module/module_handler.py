from typing import List

from pydantic import Field
from .module_abstract import ModuleAbstract
from common.models.base import BaseModel
from common.CLI.abstract_handler import AbstractHandler

import typing

class ModuleNotFound(Exception):
    pass

class ModuleHandler(AbstractHandler, BaseModel):
    """
    ModuleHandler class is a class that handles modules.
    
    Args:
        items (List[ModuleAbstract]): The modules of the handler.
    """
    items: typing.List[ModuleAbstract] = list()
    items_instance: typing.Type = Field(default=ModuleAbstract)
    
    def __init__(self, **data) -> None:
        super().__init__(**data)
        
    def _validate(self) -> None:
        super()._validate()
        
    def _validate_items(self) -> None:
        return super()._validate_items()
    
    def _validate_duplicates(self) -> None:
        return super()._validate_duplicates()
    
    def verify_item(self, item: typing.Any) -> bool:
        return super().verify_item(item)
        
    def check_item_duplicates(self, item: typing.Any) -> bool:
        return super().check_item_duplicates(item)
    
    def check_item_instance(self, item: typing.Any) -> bool:
        return super().check_item_instance(item)
            
    def add(self, module: ModuleAbstract) -> None:
        super().add(module)
        
    def extend(self, items: List[ModuleAbstract]) -> None:
        return super().extend(items)
    
    def insert(self, index: int, item: typing.Any) -> None:
        return super().insert(index, item)
            
    def remove(self, module: ModuleAbstract) -> None:
        super().remove(module)
        
    def get(self, name: str) -> ModuleAbstract:
        try:
            return super().get(name)
        except ValueError as e:
            raise ModuleNotFound(f"Module {name} not found.")
    
    def __add__(self, other: typing.Union[ModuleAbstract, typing.List[ModuleAbstract]]) -> 'ModuleHandler':
        return super().__add__(other)
    
    def execute(self, name: str, *args) -> typing.Any:
        super().execute(name, *args)
    
    def __len__(self) -> int:
        return super().__len__()
    
    def __iter__(self):
        return super().__iter__()
    
    def __lt__(self, other: 'ModuleHandler') -> bool:
        return super().__lt__(other)