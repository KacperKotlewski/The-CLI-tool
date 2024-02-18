from .module import Module

import typing

from common.CLI.option import OptionFactory, Option, OptionBuilder
from common.CLI.action import ActionFactory, ActionBuilder, ActionHandler

from common.debug import DEBUG

class RootModule(Module):
    def _extra_options_and_actions(self) -> None:
        self._append_debug_option()
        self._append_dry_run_action()
        
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
        
    def _append_dry_run_action(self) -> None:
        # add dry run action - print info about using -h or --help
        dry_run_action = ActionBuilder()
        dry_run_action.set_name("dry_run")
        dry_run_action.set_function(lambda *args: print(self.description))
        dry_run_action.set_condition(lambda *args: len(args) == 0)
        self.action_handler += dry_run_action.build()
        