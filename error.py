class ChestnutError(BaseException):
    def __init__(self, message, token=None, line=None, column=None):
        self.message=message
        self.token=token
        self.line=line
        self.column=column

    def gettype(self):
        return "Error"

    def __str__(self):
        if self.token:
           return f"{self.message} at {self.token.get_line_and_column()}"
        if self.line and self.column:
            return f"{self.message} at line {self.line}, column {self.column}"
        return f"{self.message}"

class ValueException(ChestnutError):
    pass

class TypeException(ChestnutError):
    pass

class SyntaxException(ChestnutError):
    pass

class InternalException(ChestnutError):
    pass

class RuntimeException(ChestnutError):
    pass
