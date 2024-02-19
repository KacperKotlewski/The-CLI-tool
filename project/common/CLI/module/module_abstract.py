import typing
import sys

from abc import ABC, abstractmethod

from common.CLI.abstract_model import AbstractModel
from pydantic import Field

from common.CLI.option import OptionHandler, OptionFactory, OptionValueError, Argument, Option, Flag
from common.CLI.action import ActionFactory, ActionHandler, ActionBuilder

from common.debug import DEBUG
from common.utils.settings_classes import Representation

class ModuleAbstract(AbstractModel, ABC):
    help_str: str
    option_handler: OptionHandler = None
    action_handler: ActionHandler = None
    action: typing.Callable = None
    root_module: typing.Optional['ModuleAbstract'] = None
    
    @abstractmethod
    def bad_command_action(self, *args) -> None:
        print(f"Command not found. Try '{sys.argv[0]} -h' for help.")
        
    def get_prompt_prefix(self) -> str:
        joined_args = ' '.join(sys.argv)
        command_prefix = joined_args.split(self.name)[0]
        return command_prefix
    
    @abstractmethod
    def print_help_usage_action(self, *args) -> None:
        print(f"Use '{self.get_prompt_prefix()}{self.name} -h' for help and information.")
    
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
            
    def get_value(self, name: str) -> typing.Optional[typing.Union[str, bool]]:
        """
        get_value gets the value of the option by name.
        
        Args:
            name (str): The name of the option.
            
        Returns:
            None: If the option is not set.
            str: The value of the option.
            bool: Flag value.
            
        Raises:
            ValueError: If the option is not found.
        """
        return self.option_handler.get(name).value
        
    @abstractmethod
    def _extra_options_and_actions(self) -> None:
        pass
        
    def _setup_options_and_actions(self) -> None:
        self._append_help_option()
        
        self._extra_options_and_actions()
        
    def _append_help_option(self) -> None:
        help_option = OptionFactory.flag(name='help', keys=['-h', '--help'], description='Display the help message.')
        help_action = ActionFactory.from_flag(option=help_option, function=lambda *args : (self.print_help(), exit(0)))
        self.option_handler += help_option
        self.action_handler += help_action
    
    @abstractmethod
    def execute(self, *args):
        self.execute_actions(*args)
    
    def _validate(self) -> None:
        self._validate_option_handler()
        
    def _validate_option_handler(self) -> None:
        self.option_handler._validate()
    
    def get_help(self) -> str:
        text = self.help_str + "\n\n"
        text += self.get_usage() + "\n"
        text += self.get_child_info()
        return text
    
    def print_help(self, *args) -> None:
        print(self.get_help())
        
    def get_usage(self) -> str:
        text = "Usage: \n  " + self.get_prompt_prefix() + f"{self.name}"
        text += f"{self.get_usage_args()}"
        
        return text
        
    def get_usage_args(self) -> str:
        text = ""
        
        args_ = self.option_handler.filtered(type=Argument)
        
        for arg in list(args_.filtered(required=True)):
            text += f" {arg.get_option_str()}"
        
        if len(list(args_.filtered(required=False))) > 0:
            text += f" [ARGUMENTS]"
            
        if len(self.option_handler.filtered(type=(Option, Flag))) > 0:
            text += f" [OPTIONS]"
            
        return text
            
    
    def get_child_info(self) -> str:
        Representation.set_space_upfront(2)
        Representation.set_space_between(10)
        info = ""
        
        filters = {
            "Arguments": self.option_handler.filtered(type=Argument),
            "Options": self.option_handler.filtered(type=tuple([Option, Flag])),
        }
        
        for argument in filters["Arguments"]:
            try:
                option = argument.to_option()
                filters["Options"] += option
            except ValueError:
                pass
        
        for name, filtered_items in filters.items():
            filtered_handler = OptionHandler(items = filtered_items)
            
            if len(filtered_handler) > 0:
                info += f"\n{name}:\n"
                
                strlen = max([len(opt.__repr__tuple__()[0]) for opt in filtered_handler])
                
                info += "\n".join(filtered_handler.stylized_representation(first_str_length=strlen)) +"\n"
            
        return info
        
    def describe(self) -> str:
        return self.description
    
    def print_description(self) -> None:
        print(self.describe())
                
    def execute_actions(self, *args) -> None:
        ModuleAbstract.log_strict(f"Executing actions for {self.name} with args: {args}")
        try:
            handled_args_number = self.option_handler.execute(*args)
            handled_action_number = self.action_handler.execute_actions(*args)
            self.option_handler.is_requirement_met(*args)
            
        except OptionValueError as e:
            print(f"Error: {e}\n")
            self.print_help_usage_action(*args)
            return
        
        if handled_args_number == 0 and handled_action_number == 0 and self.action is None:
            self.print_help_usage_action(*args)
        elif handled_action_number == 0:
            self.action(self, *args)
        else:
            self.bad_command_action(*args)
    
    def __call__(self, *args) -> None:
        self.execute(*args)
    
    def inherit_from(self, module: 'ModuleAbstract') -> None:
        # pass duplicate of the option and action handler
        self.root_module = module.root_module
        for option in module.option_handler:
            try:
                self.option_handler += option
            except ValueError:
                pass
        for action in module.action_handler:
            try:
                self.action_handler += action
            except ValueError:
                pass