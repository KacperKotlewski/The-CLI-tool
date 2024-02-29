from ..terminal_width import get_terminal_width

class RepresentationSettings:
    TOTAL_SPACE: int = None
    SPACE_BETWEEN: int = 1
    SPACE_UPFRONT: int = 0
    
    @staticmethod
    def set_total_space(space:int) -> None:
        RepresentationSettings.TOTAL_SPACE = space
    
    @staticmethod
    def set_space_between(space:int) -> None:
        RepresentationSettings.SPACE_BETWEEN = space
    
    @staticmethod
    def set_space_upfront(space:int) -> None:
        RepresentationSettings.SPACE_UPFRONT = space
        
    @staticmethod
    def reset_total_space() -> None:
        RepresentationSettings.TOTAL_SPACE = None
        
    @staticmethod
    def reset_space_between() -> None:
        RepresentationSettings.SPACE_BETWEEN = 1
        
    @staticmethod
    def reset_space_upfront() -> None:
        RepresentationSettings.SPACE_UPFRONT = 0
        
    @staticmethod
    def total_space() -> int:
        if RepresentationSettings.TOTAL_SPACE is None:
            return get_terminal_width()
        return RepresentationSettings.TOTAL_SPACE
    
    @staticmethod
    def space_between() -> int:
        return RepresentationSettings.SPACE_BETWEEN
    
    @staticmethod
    def space_upfront() -> int:
        return RepresentationSettings.SPACE_UPFRONT