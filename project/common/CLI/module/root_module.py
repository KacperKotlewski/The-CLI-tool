from .module import Module, ModuleHandler, ModuleAbstract

import typing

from common.CLI.option import OptionBuilder
from common.CLI.action import ActionFactory
from common.CLI.interface import InterfaceHandler, UserInterface

from common.debug import DEBUG

import sys

class RootModule(Module):
    interface_handler: InterfaceHandler = None
    root_module: typing.Optional['RootModule'] = None
    
    def __init__(self, **data) -> None:
        data['interface_handler'] = InterfaceHandler()
        super().__init__(**data)
        self.root_module = self
    
    def print_help_usage_action(self, *args) -> None:
        print(f'Use "{sys.argv[0]} -h" or "{sys.argv[0]} --help" for help and information.')
        
    def get_usage(self) -> str:
        return f'Usage: {sys.argv[0]} [command] [options]'
    
    def get_ui(self) -> UserInterface:
        return self.interface_handler.active
    
    def _extra_options_and_actions(self) -> None:
        self._append_interface_option()
        
    def activate_debug_options(self) -> None:
        self._append_debug_option()
        self._append_echo_option()
        self._append_print_option_status()
        
    def _append_print_option_status(self) -> None:
        builder = OptionBuilder().set_name('print option status')
        builder.add_key('--status')
        builder.set_description('Print the status of the options.')
        
        status_option = builder.build_flag()
        self.option_handler += status_option
        
        def print_status(*args) -> None:
            status = self.option_handler.status()
            maxlen = max([len(name) for name,status in status]); 
            print(f"Options and values: \n" + "\n".join([f"  {name:>{maxlen}s} - {value}" for name, value in status]) + "\n")
            
        
        self.action_handler.insert(0, ActionFactory.from_flag(
            option=status_option,
            function=print_status
        ))
        
    def _append_echo_option(self) -> None:
        builder = OptionBuilder().set_name('echo')
        builder.add_key('--echo')
        builder.set_description('Print the command and options to the console.')
        
        echo_option = builder.build_flag()
        self.option_handler += echo_option
        
        self.action_handler.insert(0, ActionFactory.from_flag(
            option=echo_option, 
            function=lambda *args: print(f"ECHO: \n {sys.argv}")
        ))
        
    def _append_debug_option(self) -> None:
        builder = OptionBuilder().set_name('debug')
        builder.add_key('--debug')
        builder.set_description('Enable debug mode.')
        builder.set_require_argument(False)
        builder.set_option('keyword')
        
        debug_option = builder.build_option()
        self.option_handler += debug_option
                
        self.action_handler.insert(0, ActionFactory.action(
            name='debug_flag',
            condition=lambda *args: (debug_option.to_flag().is_set()),
            function=lambda *args: DEBUG.enable()
        ))
        
        self.action_handler.insert(1, ActionFactory.from_option(
            option=debug_option, 
            condition=lambda *args: isinstance(debug_option.value, str),
            function=lambda *args: DEBUG.set_keyword(debug_option.value)
        ))
        
    def _append_interface_option(self) -> None:
        builder = OptionBuilder().set_name('interface')
        builder.add_keys('--user-interface')
        builder.set_description('Set the user interface to use. Default is CLI.')
        builder.set_option('type')
        builder.set_value('CLI')
        
        interface_option = builder.build_option()
        self.option_handler += interface_option
        
        self.action_handler.insert(0, ActionFactory.from_option(
            option=interface_option, 
            condition=lambda *args: isinstance(interface_option.value, str),
            function=lambda *args: self.interface_handler.set_active(interface_option.value)
        ))
        
    def add_interface(self, interface) -> None:
        self.interface_handler += interface
    
    def __add__(self, other: typing.Union[ModuleAbstract, typing.List[ModuleAbstract], ModuleHandler]) -> 'RootModule':
        return super().__add__(other)