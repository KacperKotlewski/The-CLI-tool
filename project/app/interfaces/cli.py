from inspect import isclass
import typing
from project.common.CLI.interface import interface, UserInterface

@interface(
    name = "CLI",
    description = "CLI interface."
)
class CLIInterface(UserInterface):
    """
    CLI interface class.
    """
    def strip_msg(self, message: str) -> str:
        try:
            if message.strip().endswith(":"):
                message = ":".join(message.split(":")[:-1])
        except:
            pass
        return message
    
    def prompt(self, message: str, required:bool=False, return_none:bool=False) -> str:
        if required and return_none:
            raise ValueError("required and return_none cannot be both True")
        
        if message is None:
            message = "Enter value"
        message = self.strip_msg(message)
        
        while True:
            input_ = input(f'{message}: ')
            if input_ != "" or (not required and input_ == "" and not return_none):
                return input_
            elif not required and input_ == "" and return_none:
                return None
            else:
                print("Value is required")
    
    def confirm(self, message: str) -> bool:
        message = self.strip_msg(message)
        input_ = input(f'{message} (y/n): ')
        return input_.lower() == "y"
    
    def choose(self, message: str, choices: typing.List[str], required:bool=False) -> int:
        message = self.strip_msg(message)
        
        print("Choose from the following options:")
        for i, choice in enumerate(choices):
            print(f"{i+1}. {choice}")
        if not required:
            print("Type 'escape' to cancel")
            
        while True:
            try:
                inp = input(f"{message}: ")
                if not required and inp.lower() == "escape":
                    return None
                choice = int(inp)
                if choice < 1 or choice > len(choices):
                    raise ValueError()
                return choice
            except ValueError:
                print("Invalid value. Input must be a number corresponding to the option")
            except KeyboardInterrupt:
                exit(0)
                
    def message(self, message: str) -> None:
        print(message)