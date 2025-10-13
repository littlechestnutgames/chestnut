from parser import *

class Symbol:
    def __init__(self, name, node, line, chestnut_type):
        self.name = name
        self.node = node
        self.chestnut_type

class Analyzer:
    def __init__(self):
        self.scopes = [{}]

    def push_scope(self):
        self.scopes.append({})

    def pop_scope(self):
        if len(self.scopes) == 1:
            raise InternalException("The global scope attempted to be popped")
        self.scopes.pop()

    def get_current(self):
        return self.scopes[-1]

    def find_first_scope_containing(self, var_name):
        for scope in reversed(self.scopes):
            if var_name in scope:
                return scope
        return None

    def analyze(self, ast):
        pass
