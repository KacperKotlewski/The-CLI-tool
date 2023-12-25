class EnvSchemaNotFound(Exception):
    """Exception raised when the environment schema file is not found."""
    def __init__(self, message="Environment schema file not found"):
        self.message = message
        super().__init__(self.message)

class EnvSchemaNotValidVersion(Exception):
    """Exception raised when the schema version is not valid."""
    def __init__(self, version, message="Not a valid schema version"):
        self.version = version
        self.message = f"{message}: {version}"
        super().__init__(self.message)

class EnvSchemaNoSchemaInfo(Exception):
    """Exception raised when schema information is missing."""
    def __init__(self, message="No schema information found"):
        self.message = message
        super().__init__(self.message)

class EnvSchemaBadElement(Exception):
    """Exception raised for a bad element in the schema."""
    def __init__(self, element, message="Bad element in schema"):
        self.element = element
        self.message = f"{message}: {element}"
        super().__init__(self.message)

class EnvSchemaBadTextType(Exception):
    """Exception raised for an invalid text type in the schema."""
    def __init__(self, text_type, message="Bad text type in schema"):
        self.text_type = text_type
        self.message = f"{message}: {text_type}"
        super().__init__(self.message)

class EnvSchemaBadFieldValue(Exception):
    """Exception raised for a bad field value in the schema."""
    def __init__(self, field, message="Bad field value"):
        self.field = field
        self.message = f"{message}: {field}"
        super().__init__(self.message)

class EnvSchemaBadFieldProp(Exception):
    """Exception raised for a bad field property in the schema."""
    def __init__(self, prop, message="Bad field property"):
        self.prop = prop
        self.message = f"{message}: {prop}"
        super().__init__(self.message)
        
class EnvSchemaParsingError(Exception):
    """Exception raised for a issue with parsing schema"""
    def __init__(self, prop, message="Error while parsing"):
        self.prop = prop
        self.message = f"{message}: {prop}"
        super().__init__(self.message)