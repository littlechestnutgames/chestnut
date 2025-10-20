from error import *
from lexer import Token
from functools import wraps

def comparison_operation(op_symbol, op_name, reverse=False):
    def decorator(func):
        @wraps(func)
        def wrapper(self, other):
            self.__typecheck__(other, op_name)
            left = self.value if not reverse else other.value
            right = other.value if not reverse else self.value
            return ChestnutBoolean(left.__getattribute__(op_symbol)(right))
        return wrapper
    return decorator

def numeric_operation(op_symbol, op_name, reverse=False):
    def decorator(func):
        @wraps(func)
        def wrapper(self, other):
            if func.__name__ == "__add__" and isinstance(other, ChestnutString):
                return NotImplemented
            self.__typecheck__(other, op_name)
            if func.__name__.endswith("div__") or func.__name__.endswith("mod__"):
                divisor = self.value if reverse else other.value
                if divisor == 0:
                    raise RuntimeException("Cannot divide by 0")
            left = self.value if not reverse else other.value
            right = other.value if not reverse else self.value
            return type(self)(left.__getattribute__(op_symbol)(right))
        return wrapper
    return decorator

class ChestnutAny:
    def __init__(self, token):
        if hasattr(token, "data"):
             self.value = token.data
             self.token = token
        else:
            self.value = token
            self.token = token

    def __str__(self):
        return str(self.value)

    def __typecheck__(self, other, op):
        other_type = type(other).__name__
        if isinstance(other, ChestnutAny):
            other_type = other.gettype()
        if not type(self) == type(other):
            raise TypeException(f"Attempted to {op} {self.gettype()} and {other_type}")

    def gettype(self):
        import re
        t = type(self).__name__.replace("Chestnut", "")
        return t

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

    def properties(self):
        raise TypeException("Unsupported type", token=self.token)

    def token_matches(self, token_label):
        return self.token.label == token_label

    def isnull(self):
        return False

    def __eq__(self, other):
        self.__typecheck__(other, "equals")
        return self.value == other.value

class ChestnutString(ChestnutAny):
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

        if isinstance(other, ChestnutAny):
            value = other.value

        return ChestnutString(Token("String", self.value + str(value), None, None))

    def __radd__(self, other):
        value = other
        
        if isinstance(other, ChestnutAny):
            value = other.value

        return ChestnutString(Token("String", self.value + str(value), None, None))

    def __eq__(self, other):
        return str(self) == str(other)

    def __len__(self):
        return len(self.value)

    def __repr__(self):
        return f"ChestnutString({self.value})"

class ChestnutNull(ChestnutAny):
    def isnull(self):
        return True

    def __str__(self):
        return "null"

class ChestnutBoolean(ChestnutAny):
    def isbool(self):
        return True
    def __bool__(self):
        return self.value

class ChestnutNumber(ChestnutAny):
    MIN = 0
    MAX = 0
    def isnumeric(self):
        return True

    @numeric_operation("__add__", "add")
    def __add__(self, other): pass

    @numeric_operation("__radd__", "add", reverse=True)
    def __radd__(self, other): pass

    @numeric_operation("__sub__", "sub")
    def __sub__(self, other): pass

    @numeric_operation("__rsub__", "sub", reverse=True)
    def __rsub__(self, other): pass

    @numeric_operation("__truediv__", "divide")
    def __truediv__(self, other): pass

    @numeric_operation("__rtruediv__", "divide", reverse=True)
    def __rtruediv__(self, other): pass

    @numeric_operation("__mul__", "multiply")
    def __mul__(self, other): pass

    @numeric_operation("__rmul__", "multiply", reverse=True)
    def __rmul__(self, other): pass

    @numeric_operation("__pow__", "exponentiate")
    def __pow__(self, other): pass

    @numeric_operation("__rpow__", "exponentiate", reverse=True)
    def __rpow__(self, other): pass

    @numeric_operation("__xor__", "xor")
    def __xor__(self, other): pass

    @numeric_operation("__rxor__", "xor", reverse=True)
    def __rxor__(self, other): pass

    @comparison_operation("__lt__", "less than")
    def __lt__(self, other): pass

    @comparison_operation("__rlt__", "less than", reverse=True)
    def __rlt__(self, other): pass

    @comparison_operation("__gt__", "greater than")
    def __gt__(self, other): pass

    @comparison_operation("__rgt__", "greater than", reverse=True)
    def __rgt__(self, other): pass

    @comparison_operation("__lte__", "less than or equal to")
    def __lte__(self, other): pass

    @comparison_operation("__rlte__", "less than or equal to", reverse=True)
    def __rlte__(self, other): pass

    @comparison_operation("__gte__", "greater than or equal to")
    def __gte__(self, other): pass

    @comparison_operation("__rgte__", "greater than or equal to", reverse=True)
    def __rgte__(self, other): pass

class ChestnutInteger(ChestnutNumber):
    def isint(self):
        return True

    def __bitwise_shift_lengthcheck__(self, shift_amount_operand):
        if shift_amount_operand.value < 0:
            raise ValueException("Shift amount must be greater than 0")

    def __bitwise_shift_typecheck__(self, other):
        if not isinstance(other, ChestnutInteger):
            raise TypeException("Shift amount must be specified in an Integer type")
        self.__bitwise_shift_lengthcheck__(other)

    def __lshift__(self, other):
        self.__bitwise_shift_typecheck__(other)
        return type(self)(self.value << other.value)

    def __rlshift__(self, other):
        self.__bitwise_shift_lengthcheck__(self)
        if not isinstance(other, ChestnutInteger):
            raise TypeException("Lefthand value must be an Integer type")
        return type(self)(other.value << self.value)

    def __rshift__(self, other):
        self.__bitwise_shift_typecheck__(other)
        return type(self)(self.value >> other.value)

    def __rrshift__(self, other):
        self.__bitwise_shift_lengthcheck__(self)
        if not isinstance(other, ChestnutInteger):
            raise TypeException("Lefthand value must be an Integer type")
        return type(self)(other.value >> self.value)

    def __invert__(self):
        return ChestnutInteger(~self.value)

    def __and__(self, other):
        self.__typecheck__(other, "&")
        return ChestnutInteger(self.value & other.value)

    def __or__(self, other):
        self.__typecheck__(other, "|")
        return ChestnutInteger(self.value | other.value)

    def __xor__(self, other):
        self.__typecheck__(other, "^")
        return ChestnutInteger(self.value ^ other.value)

    def __str__(self):
        return str(self.value)

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

class ChestnutList(ChestnutAny):
    def __init__(self, token, bound_type=ChestnutAny):
        super().__init__(token)
        if not issubclass(bound_type, ChestnutAny):
            raise RuntimeException(f"{bound_type.__name__} is not a Chestnut type")
        self.bound_type = bound_type

    def length(self):
        return ChestnutInteger(len(self.value))

    def __len__(self):
        return len(self.value)

    def __getitem__(self, var_name):
        return self.value[var_name]

    def __setitem__(self, var_name, value):
        if not isinstance(value, self.bound_type):
            raise TypeException(f"Item inserted into Chestnut list must be a Chestnut {self.bound_type}")

        self.value[var_name] = value

    def __iter__(self):
        return iter(self.value)

    def __contains__(self, var_name):
        return ChestnutBoolean(var_name in self.value)

    def __repr__(self):
        return f"ChestnutList(<{self.value}>)"

    def append(self, value):
        self.value.append(value)

    def extend(self, items):
        self.value.extend(items)

    def insert(self, index, item):
        self.value.insert(index, item)

    def remove(self, item):
        self.value.remove(item)

    def pop(self, index):
        return self.value.pop(index)

class ChestnutStruct(ChestnutAny):
    def length(self):
        return len(self.value)

class ChestnutTuple(ChestnutAny):
    def length(self):
        return ChestnutInteger(len(self.value))

    def __len__(self):
        return len(self.value)
    def __getitem__(self, index):
        return self.value[index]
