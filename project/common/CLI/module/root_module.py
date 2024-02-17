from .module import Module

import typing

from common.CLI.option import OptionFactory
from common.CLI.action import ActionFactory, ActionBuilder

from common.debug import DEBUG

class RootModule(Module):
    def _extra_options_and_actions(self) -> None:
        debug_flag = OptionFactory.flag(name='debug', keys=['--debug'], description='Enable debug mode.')
        self.option_handler += debug_flag
        self.action_handler += ActionFactory.from_flag(option=debug_flag, function=lambda *args: DEBUG.enable())
        
        # add dry run action - print info about using -h or --help
        dry_run_action = ActionBuilder()
        dry_run_action.set_name("dry_run")
        dry_run_action.set_function(lambda *args: print(self.description))
        dry_run_action.set_condition(lambda *args: len(args) == 0)
        self.action_handler += dry_run_action.build()
        