import enum
from copy import deepcopy
import typing
import sys

from abc import ABC, abstractmethod

from common.CLI.abstract_model import AbstractModel
from pydantic import Field

from common.CLI.option import OptionHandler, OptionFactory
from common.CLI.action import ActionFactory, ActionHandler
# from common.CLI.interface import UserInterface

from common.debug import DEBUG

class ModuleAbstract(AbstractModel, ABC):
    help_str: str = None
    option_handler: OptionHandler = None
    action_handler: ActionHandler = None
    default_action: typing.Callable = Field(default=lambda *args: print(f"Command not found. Try '{sys.argv[0]} -h' for help."))
    # current_user_interface: 'UserInterface' = None
    
    def __init__(self, **data) -> None:
        option_handler = data.get('option_handler', None)
        action_handler = data.get('action_handler', None)
        data['option_handler'] = OptionHandler()
        data['action_handler'] = ActionHandler()
        
        super().__init__(**data)
        
        self._setup_options_and_actions()
        
        self._extra_options_and_actions()
        
        if option_handler:
            self.option_handler += option_handler
        if action_handler:
            self.action_handler += action_handler
        
    @abstractmethod
    def _extra_options_and_actions(self) -> None:
        pass
        
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
        print(f"\n{self.get_help()}")
        print(self.get_details())
            
    
    def get_details(self) -> str:
        info = ""
        
        try:
            from blessed import Terminal
            term = Terminal()
            width = term.width
        except ImportError:
            import shutil
            width = shutil.get_terminal_size().columns
            
        spaces = {"before": 2, "after": 10}
        
        calc_taken = lambda strlen: spaces["before"] + strlen + spaces["after"]
        
        create_str = lambda text1, text2: (
            " " * spaces["before"] +
            text1 +
            " " * spaces["after"] +
            text2
        )
        
        if len(self.option_handler) > 0:
            info += f"\nOptions:\n"
            strlen = max([len(opt.get_keys_str()) for opt in self.option_handler.options])
            
            taken = calc_taken(strlen)
            
            create_opt_str = lambda option: create_str(option.get_stylized_keys(strlen), option.spaced_description(taken, width)[taken+1:])
            
            info += "\n".join([create_opt_str(opt) for opt in self.option_handler.options]) +"\n"
            
        return info
        
    def describe(self) -> str:
        return self.description
    
    def print_description(self) -> None:
        print(self.describe())
        
    # get args and go through options with option_handler.handle_args()
    def handle_args(self, *args) -> int:
        if len(args) == 0:
            return
        return self.option_handler.handle_args(*args)
        
    def execute_actions(self, *args) -> None:
        handled_args_number = self.handle_args(*args)
        handled_action_number = self.action_handler.execute_actions(*args)

        if handled_args_number == 0 and handled_action_number == 0:
            self.default_action(*args)
    
    def __call__(self, *args) -> None:
        self.execute(*args)
    
    def inherit_from(self, module: 'ModuleAbstract') -> None:
        self.option_handler += module.option_handler
        self.action_handler += module.action_handler