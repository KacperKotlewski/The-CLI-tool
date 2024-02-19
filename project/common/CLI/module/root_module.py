from pydantic import Field
from .module import Module

import typing

from common.CLI.option import OptionFactory, Option, OptionBuilder
from common.CLI.action import ActionFactory, ActionBuilder, ActionHandler
from common.CLI.interface import InterfaceHandler

from common.SOLID import Singleton
from common.debug import DEBUG

import sys

class RootModule(Singleton, Module):
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
    
    def _extra_options_and_actions(self) -> None:
        self._append_debug_option()
        self._append_interface_option()
        
    def _append_debug_option(self) -> None:
        builder = OptionBuilder().set_name('debug')
        builder.add_key('--debug')
        builder.set_description('Enable debug mode.')
        builder.set_require_argument(False)
        builder.set_option('keyword')
        
        debug_option = builder.build_option()
        self.option_handler += debug_option
                
        self.action_handler.insert_action(0, ActionFactory.action(
            name='debug_flag',
            condition=lambda *args: (debug_option.to_flag().is_set()),
            function=lambda *args: DEBUG.enable()
        ))
        
        self.action_handler.insert_action(1, ActionFactory.from_option(
            option=debug_option, 
            condition=lambda *args: isinstance(debug_option.value, str),
            function=lambda *args: DEBUG.set_keyword(debug_option.value)
        ))
        
    def _append_interface_option(self) -> None:
        builder = OptionBuilder().set_name('interface')
        builder.add_keys('-U', '--user-interface')
        builder.set_description('Set the user interface to use. Default is cli.')
        builder.set_option('type')
        builder.set_value('cli')
        
        interface_option = builder.build_option()
        self.option_handler += interface_option
        
        # self.action_handler.insert_action(0, ActionFactory.from_option(
        #     option=interface_option, 
        #     condition=lambda *args: isinstance(interface_option.value, str),
        #     function=lambda *args: self.interface_handler.set_active(interface_option.value)
        # ))
    
    # def get_ui(self) -> 'UserInterface':
    #     return self.interface_handler.active