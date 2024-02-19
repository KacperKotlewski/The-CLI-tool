from .module import Module

import typing

from common.CLI.option import OptionFactory, Option, OptionBuilder
from common.CLI.action import ActionFactory, ActionBuilder, ActionHandler

from common.debug import DEBUG

import sys

class RootModule(Module):
    
    def print_help_usage_action(self, *args) -> None:
        print(f'Use "{sys.argv[0]} -h" or "{sys.argv[0]} --help" for help and information.')
        
    def get_usage(self) -> str:
        return f'Usage: {sys.argv[0]} [command] [options]'
    
    def _extra_options_and_actions(self) -> None:
        self._append_debug_option()
        
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
        