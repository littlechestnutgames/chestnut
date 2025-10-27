from error import *
from lexer import Token
from functools import wraps
# In chestnut_type.py:

def comparison_operation(op_symbol, op_name, reverse=False):
    def decorator(func):
        @wraps(func)
        def wrapper(self, other):
            self.__typecheck__(other, op_name)
            left = self.value if not reverse else other.value
            right = other.value if not reverse else self.value
            
            raw_result = left.__getattribute__(op_symbol)(right)
            
            return raw_result
        return wrapper
    return decorator

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

def chestnut_wrapper(magic_method_name, chestnut_type_wrapper):
    def decorator(func):
        @wraps(func)
        def wrapper(self, other):
            chestnut_type = eval(chestnut_type_wrapper)
            magic_method = getattr(self, magic_method_name)
            raw_result = magic_method(other)
            if magic_method_name in ("__and__", "__or__"):
                raw_result = bool(raw_result)
            if not isinstance(raw_result, ChestnutAny):
                return chestnut_type(raw_result)
            return raw_result
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
                divisor = self if reverse else other
                if divisor == ChestnutInteger(0):
                    raise RuntimeException("Cannot divide by 0")
            left = self.value if not reverse else other.value
            right = other.value if not reverse else self.value
            return type(self)(left.__getattribute__(op_symbol)(right))
        return wrapper
    return decorator

class ChestnutAny:
    def __bool__(self):
        return False
    def __init__(self,token=None):
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

    def equals(self, other):
        return ChestnutBoolean(self.__eq__(other))

    def nequals(self, other):
        return ChestnutBoolean(self.__ne__(other))

    def __eq__(self, other):
        if isinstance(self, ChestnutNull) or isinstance(other, ChestnutNull):
            return ChestnutBoolean(isinstance(self, ChestnutNull) and isinstance(other, ChestnutNull))

        if not isinstance(other, ChestnutAny):
            raise Exception(f"Chestnut types must compare to Chestnut types. Given { type(other) }")

        self.__typecheck__(other, "equals")
        return ChestnutBoolean(self.value == other.value)

    def __ne__(self, other):
        return ChestnutBoolean(not self.__eq__(other))

    @chestnut_wrapper("__or__", "ChestnutBoolean")
    def wrapped_or(self, other): pass

    def __or__(self, other):
        return self.value or other.value

    @chestnut_wrapper("__and__", "ChestnutBoolean")
    def wrapped_and(self, other): pass

    def __and__(self, other):
        return self.value and other.value

class ChestnutString(ChestnutAny):
    def isstring(self):
        return True

    def isbool(self):
        return False

    def length(self):
        return len(self.value)

    def __getitem__(self, item):
        if not isinstance(item, ChestnutInteger):
            raise Exception(item.__repr__())
            raise RuntimeException("Attempt to access a non-Integer index on a string", self.token)
        return self.value[item.value]

    def __setitem__(self, item, value):
        if not isinstance(item, ChestnutInteger):
            raise RuntimeException("Attempt to set non-Integer index on a String", self.token)
        if not isinstance(value, ChestnutString):
            raise RuntimeException("Attempt to set non-String value on a String", self.token)

        self.value[item.value] = value.value

    def addition(self, other):
        value = self.__add__(other)
        if not isinstance(value, ChestnutString):
            value = ChestnutString(value)
        return value

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
        other_value = str(other)
        if isinstance(other, ChestnutAny):
            other_value = str(other.value)

        return ChestnutBoolean(str(self.value) == str(other_value))

    def __len__(self):
        return len(self.value)

    def __repr__(self):
        return f"ChestnutString({self.value})"

    def __bool__(self):
        return len(self.value) > 0

class ChestnutNull(ChestnutAny):
    def isnull(self):
        return True

    def __str__(self):
        return "null"

    def __bool__(self):
        return False

class ChestnutBoolean(ChestnutAny):
    def isbool(self):
        return True

    def __bool__(self):
        return self.value

    def __str__(self):
        if self.value:
            return "true"
        return "false"

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

    @numeric_operation("__mod__", "mod")
    def __mod__(self, other): pass

    @numeric_operation("__rmod__", "mod", reverse=True)
    def __rmod__(self, other): pass

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

    def less_than(self, other):
        return ChestnutBoolean(self.__lt__(other))

    @comparison_operation("__rlt__", "less than", reverse=True)
    def __rlt__(self, other): pass

    def rightside_less_than(self, other):
        return ChestnutBoolean(self.__rlt__(other))

    @comparison_operation("__gt__", "greater than")
    def __gt__(self, other): pass

    def greater_than(self, other):
        return ChestnutBoolean(self.__gt__(other))

    @comparison_operation("__rgt__", "greater than", reverse=True)
    def __rgt__(self, other): pass

    def rightside_greater_than(self, other):
        return ChestnutBoolean(self.__rgt__(other))

    @comparison_operation("__le__", "less than or equal to")
    def __le__(self, other): pass

    def less_than_or_equal_to(self, other):
        return ChestnutBoolean(self.__le__(other))

    @comparison_operation("__rle__", "less than or equal to", reverse=True)
    def __rle__(self, other): pass

    def rightside_less_than_or_equal_to(self, other):
        return ChestnutBoolean(self.__rle__(other))

    @comparison_operation("__ge__", "greater than or equal to")
    def __ge__(self, other): pass

    def greater_than_or_equal_to(self, other):
        return ChestnutBoolean(self.__ge__(other))

    @comparison_operation("__rge__", "greater than or equal to", reverse=True)
    def __rge__(self, other): pass

    def rightside_greater_than_or_equal_to(self, other):
        return ChestnutBoolean(self.__rge__(other))

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

    def addition(self, other):
        value = self.__add__(other)
        if not isinstance(value, ChestnutInteger):
            value = ChestnutInteger(value)
        return value

    def subtraction(self, other):
        value = self.__sub__(other)
        if not isinstance(value, ChestnutInteger):
            value = ChestnutInteger(value)
        return value

    def division(self, other):
        value = self.__truediv__(other)
        if not isinstance(value, ChestnutInteger):
            value = ChestnutInteger(value)
        return value

    def multiplication(self, other):
        value = self.__mul__(other)
        if not isinstance(value, ChestnutInteger):
            value = ChestnutInteger(value)
        return value

    def modulos(self, other):
        value = self.__mod__(other)
        if not isinstance(value, ChestnutInteger):
            value = ChestnutInteger(value)
        return value

    def exponentiation(self, other):
        value = self.__pow__(other)
        if not isinstance(value, ChestnutInteger):
            value = ChestnutInteger(value)
        return value

    def __bool__(self):
        return self.value != 0



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

    def __bool__(self):
        return length(self.value) > 0

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

class ChestnutFileHandle(ChestnutAny):
    def __init__(self, file_object, token=None):
        if not hasattr(file_object, 'read') or not hasattr(file_object, 'close'):
            raise InternalException("File object must support read and close methods.")
        super().__init__(file_object)

    def __repr__(self):
        try:
            name = self.value.name
            mode = self.value.mode
        except ValueError:
            name = "CLOSED"
            mode = "N/A"

        return f"ChestnutFileHandle(name='{name}', mode='{mode}')"

    def gettype(self):
        return "FileHandle"

    def close(self):
        if not self.value.closed:
            self.value.close()
            return ChestnutBoolean(True)
        return ChestnutBoolean(False)

