class DEBUG:
    debug_mode = False
    _instance = None
    keyword = "DEBUG"

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @staticmethod
    def log(*args, **kwargs):
        if DEBUG.debug_mode:
            print(*args, **kwargs)
            
    def dlog(*args, **kwargs):
        DEBUG.log("DEBUG: ", *args, **kwargs)
            
    @staticmethod
    def conditional_log(condition: bool, *args, **kwargs):
        if condition:
            DEBUG.dlog(*args, **kwargs)
            
    @staticmethod
    def log_matching_keyword(keyword: str, *args, **kwargs):
        DEBUG.conditional_log(keyword == DEBUG.keyword, *args, **kwargs)

    @staticmethod
    def set_debug_mode(debug_mode: bool):
        DEBUG.debug_mode = debug_mode
        DEBUG.log("Debug mode:", DEBUG.debug_mode)
        return DEBUG.debug_mode
    
    @staticmethod
    def enable():
        return DEBUG.set_debug_mode(True)
    
    @staticmethod
    def disable():
        return DEBUG.set_debug_mode(False)
    
    @staticmethod
    def set_keyword(keyword: str):
        DEBUG.keyword = keyword
        DEBUG.log("Keyword:", DEBUG.keyword)
        return DEBUG.keyword
    
debug = DEBUG()
def log(*args, **kwargs):
    debug.dlog(*args, **kwargs)
    
def log_section(section: str, *args, **kwargs):
    debug.log_matching_keyword(section, *args, **kwargs)
    