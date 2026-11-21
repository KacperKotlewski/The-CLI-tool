import os
import re
import sys
from common.CLI.module import Module, Command, command
from common.CLI.option import OptionFactory, OptionBuilder, OptionHandler
from common.CLI.module.root_module import RootModule
from common.CLI.interface import UserInterface

@command(
    name = "Example",
    description = "This is an example command.",
    help_str = "This command is an example of how to create a command.",
    option_handler = [
         OptionFactory.argument(
            name='input',
            keys=['-i', '--input'],
            description='Input .env file to deserialize.',
            required=True
        ),
    ]
)
def fake_cmd(self: Command, *args, **kwargs) -> Command:
    root:RootModule = self.root_module
    ui:UserInterface = root.get_ui()
    
    ui.message("Hello")
    ui.prompt("What are you wishing for honey?")
    ui.choose("Choose a number", ["1", "2", "3"])
    ui.confirm("Is this boring enough for you?")
    
    