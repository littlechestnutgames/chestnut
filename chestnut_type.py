from error import *
from lexer import Token
class ChestnutType:
    def __init__(self, token):
        self.value = token.data
        self.token = token

    def isstring(self):
        return False

    def isbool(self):
        return False

    def isnumeric(self):
        return False

    def isint(self):
        return False

    def isfloat(self):
        return False

    def isunsigned(self):
        return False

    def islist(self):
        return False

    def length(self):
        return None

    def gettype(self):
        return "ChestnutType"

    def properties(self):
        raise TypeException("Unsupported type", token=self.token)

    def token_matches(self, token_label):
        return self.token.label == token_label

    def isnull(self):
        return False

class ChestnutString(ChestnutType):
    def gettype(self):
        return "ChestnutString"

    def isstring(self):
        return True

    def isbool(self):
        return False

    def length(self):
        return len(self.value)

    def __add__(self, other):
        value = other
        
        if hasattr(other,"value"):
            value = other.value

        return ChestnutString(Token("String", self.value + str(value), None, None))

    def __radd__(self, other):
        value = other
        
        if hasattr(other,"value"):
            value = other.value
        return ChestnutString(Token("String", self.value + str(value), None, None))
    def __str__(self):
        return self.value

    def __repr__(self):
        return f"ChestnutString({self.value})"

class ChestnutNull(ChestnutType):
    def isnull(self):
        return True
    def __str__(self):
        return "null"

class ChestnutBoolean(ChestnutType):
    def isbool(self):
        return True

class ChestnutNumber(ChestnutType):
    MIN = 0
    MAX = 0
    def isnumeric(self):
        return True

class ChestnutInteger(ChestnutNumber):
    def isint(self):
        return True

class ChestnutInt8(ChestnutInteger):
    MIN = -2**7
    MAX = 2**7-1

class ChestnutInt16(ChestnutInteger):
    MIN = -2**15
    MAX = 2**15-1

class ChestnutInt32(ChestnutInteger):
    MIN = -2**31
    MAX = 2**31-1

class ChestnutInt64(ChestnutInteger):
    MIN = -2**63
    MAX = 2**63-1

class ChestnutInt128(ChestnutInteger):
    MIN = -2**128
    MAX = 2**128-1

class ChestnutUnsignedInteger(ChestnutInteger):
    MASK = 0x0
    def isunsigned(self):
        return True

class ChestnutUInt8(ChestnutUnsignedInteger):
    MASK = 0xFF
    MAX = 2**8-1

class ChestnutUInt16(ChestnutUnsignedInteger):
    MASK = 0xFFFF
    MAX = 2**16-1

class ChestnutUInt32(ChestnutUnsignedInteger):
    MASK = 0xFFFFFFFF
    MAX = 2**32-1

class ChestnutUInt64(ChestnutUnsignedInteger):
    MASK = 0xFFFFFFFFFFFFFFFF
    MAX = 2**64-1

class ChestnutUInt128(ChestnutUnsignedInteger):
    MASK = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
    MAX = 2**128-1

class ChestnutFloat(ChestnutNumber):
    def isfloat(self):
        return True

class ChestnutFloat32(ChestnutFloat):
    MIN = -3.4028235 * 10**38
    MAX = 3.4028235 * 10**38

class ChestnutFloat64(ChestnutFloat):
    MIN = -1.7976931348623157 * 10**38
    MAX = 1.7976931348623157 * 10**38

class ChestnutList(ChestnutType):
    def length(self):
        return len(self.value)

class ChestnutStruct(ChestnutType):
    def length(self):
        return len(self.value)

class ChestnutTuple(ChestnutType):
    def length(self):
        return len(self.value)
