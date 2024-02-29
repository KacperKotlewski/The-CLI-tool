class OptionValueError(ValueError):
    pass

class OptionNotSetError(OptionValueError):
    pass

class OptionNotValidError(OptionValueError):
    pass

class ArgumentNotValidError(OptionValueError):
    pass