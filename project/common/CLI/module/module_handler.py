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
        
    def get(self, name: str) -> ModuleAbstract:
        try:
            return super().get(name)
        except ValueError as e:
            raise ModuleNotFound(f"Module {name} not found.")
    
    def filtered(self, condition: typing.Callable = None, type: typing.Type = None) -> 'ModuleHandler':
        return super().filtered(condition, type=type)
    
    def execute(self, name: str, *args) -> typing.Any:
        return super().execute(name, *args)