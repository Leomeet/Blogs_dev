# user defined Exceptions

class LlmModelSelectionException(Exception):
    """ Raised when having issue of selecting llm model"""
    pass

class EmptyModelSelectionException(Exception):
    """ Raised when No model is selected"""
    pass

class MissingKeysException(Exception):
    """ Raised when required keys to access a model is/are not available """
    pass

class DatabaseException(Exception):
    """ Raised when any database operation went wrong"""
    pass