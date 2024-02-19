import typing

from .interface_class import Interface




T = typing.Union[Interface]
# universal decorator to create new command
def user_interface(name: str, description: str) -> typing.Callable:
    def decorator(element: T) -> Interface:
        from ..module.root_module import RootModule
        root = RootModule()
        
        if isinstance(element, typing.Callable):
            return Interface(name=name, description=description)
        
        else:
            raise ValueError(f"Element '{element}' is not recognized.")
        
    return decorator