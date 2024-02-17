import enum
from copy import deepcopy
import typing

from abc import ABC, abstractmethod

from common.models.base import BaseModel

from common.CLI.option import OptionHandler, OptionFactory
from common.CLI.action import ActionFactory, ActionHandler
# from common.CLI.interface import UserInterface

class ModuleAbstract(BaseModel, ABC):
    name: str = None
    description: str = None
    help_str: str = None
    option_handler: OptionHandler = None
    current_user_interface: 'UserInterface' = None
    action_handler: ActionHandler = None
    
    def __init__(self, **data) -> None:
        self._setup_options_and_actions()
        super().__init__(**data)
        
    def _setup_options_and_actions(self) -> None:
        self.option_handler = OptionHandler()
        self.action_handler = ActionHandler()
        #add help option
        help_option = OptionFactory.flag(name='help', keys=['-h', '--help'], description='Display the help message.')
        help_action = ActionFactory.from_flag(name='help', function=self.print_help, condition=self.option_handler.is_option_set('help'))
        self.option_handler += help_option
        self.action_handler += help_action
    
    @abstractmethod
    def execute(self, *args):
        pass
    
    def _validate(self) -> None:
        self._validate_option_handler()
        
    def _validate_option_handler(self) -> None:
        self.option_handler._validate()
    
    def get_help(self) -> str:
        return self.help_str
    
    def print_help(self) -> None:
        print(self.get_help())
        print(self.option_handler.get_help())
        
    # get args and go through options with option_handler.handle_args()
    def handle_args(self, args: typing.List[str]) -> None:
        self.option_handler.handle_args(args)
        
    def execute_actions(self, args: typing.List[str]) -> None:
        self.handle_args(args)
        self.action_handler.execute_actions()
    
    def __call__(self, *args: enum.Any) -> enum.Any:
        return self.execute(*args)
    
    def inherit_from(self, module: 'ModuleAbstract') -> None:
        self.option_handler += module.option_handler
        self.action_handler += module.action_handler