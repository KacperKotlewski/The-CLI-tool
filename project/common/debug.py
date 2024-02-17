class DEBUG:
    debug_mode = False

    @staticmethod
    def log(*args, **kwargs):
        if DEBUG.debug_mode:
            print(*args, **kwargs)

    @staticmethod
    def set_debug_mode(debug_mode: bool):
        DEBUG.debug_mode = debug_mode
        return DEBUG.debug_mode
    
    @staticmethod
    def enable():
        return DEBUG.set_debug_mode(True)
    
    @staticmethod
    def disable():
        return DEBUG.set_debug_mode(False)
    