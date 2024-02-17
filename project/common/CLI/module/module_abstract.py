import enum
from copy import deepcopy
import typing

from abc import ABC, abstractmethod

from common.models.base import BaseModel
from pydantic import Field

from common.CLI.option import OptionHandler, OptionFactory
from common.CLI.action import ActionFactory, ActionHandler
# from common.CLI.interface import UserInterface

class ModuleAbstract(BaseModel, ABC):
    name: str = None
    description: str = None
    details: str = None
    help_str: str = None
    option_handler: OptionHandler = Field(default_factory=OptionHandler)
    action_handler: ActionHandler = Field(default_factory=ActionHandler)
    # current_user_interface: 'UserInterface' = None
    
    def __init__(self, **data) -> None:
        option_handler = data.get('option_handler', None)
        action_handler = data.get('action_handler', None)
        data['option_handler'] = OptionHandler()
        data['action_handler'] = ActionHandler()
        
        super().__init__(**data)
        self._setup_options_and_actions()
        
        if option_handler:
            self.option_handler += option_handler
        if action_handler:
            self.action_handler += action_handler
        
    def _setup_options_and_actions(self) -> None:
        #add help option
        help_option = OptionFactory.flag(name='help', keys=['-h', '--help'], description='Display the help message.')
        help_action = ActionFactory.from_flag(option=help_option, function=self.print_help)
        self.option_handler += help_option
        self.action_handler += help_action
        #add description action when no arguments are passed
        # description_action = ActionFactory.action(name='describe', function=self.print_description, condition=lambda *args: len(args) == 0)
        # self.action_handler += description_action
    
    @abstractmethod
    def execute(self, *args):
        self.execute_actions(*args)
    
    def _validate(self) -> None:
        self._validate_option_handler()
        
    def _validate_option_handler(self) -> None:
        self.option_handler._validate()
    
    def get_help(self) -> str:
        return self.help_str
    
    def print_help(self, *args) -> None:
        print(self.get_help())
        print(self.option_handler.get_help())
        
    def describe(self) -> str:
        return self.description
    
    def print_description(self) -> None:
        print(self.describe())
        
    # get args and go through options with option_handler.handle_args()
    def handle_args(self, *args) -> None:
        if len(args) == 0:
            return
        self.option_handler.handle_args(*args)
        
    def execute_actions(self, *args) -> None:
        self.handle_args(*args)
        self.action_handler.execute_actions(*args)
    
    def __call__(self, *args) -> None:
        self.execute(*args)
    
    def inherit_from(self, module: 'ModuleAbstract') -> None:
        self.option_handler += module.option_handler
        self.action_handler += module.action_handler