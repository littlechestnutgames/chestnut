class Token:
    def __init__(self, label, data, line, column):
        self.label = label
        self.data = data
        self.line = line
        self.column = column

    def get_line_and_column(self):
        return f"line {self.line}, column {self.column}"

    def __repr__(self):
        return f"Token({self.label}, {self.data}, {self.line}, {self.column})"

class TokenType:
    def __init__(self, name, sequence, default_value=None):
        self.name = name
        self.sequence = sequence
        self.default_value = default_value
