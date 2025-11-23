from chestnut_types import *
from error import *

def __internal_print__(*args):
    print(*args, end='')
    return CHESTNUT_NULL

def __internal_printline__(*args):
    print(*args)
    return CHESTNUT_NULL

def __internal_length__(a):
    return ChestnutInteger(len(a))

def __internal_readline__():
    return ChestnutString(input())

def __internal_insert__(l, a, i):
    index = i
    if isinstance(i, ChestnutInteger):
        index = i.value
    l.insert(index, a)
    return CHESTNUT_NULL

def __internal_remove__(l, i):
    index = i
    if isinstance(i, ChestnutInteger):
        index = i.value
    return l.pop(index)

def __internal_type__(o):
    if isinstance(o, ChestnutAny):
        return f"{o.gettype()}"
    return str("Python " + str(type(o)))

def __internal_open_file__(path, mode):
    if not isinstance(path, ChestnutString) or not isinstance(mode, ChestnutString):
        return (CHESTNUT_NULL, ChestnutError("File path and mode must be strings"))
    
    try:
        file_object = open(path.value, mode.value)
        return (ChestnutFileHandle(file_object), CHESTNUT_NULL)
    except FileNotFoundError:
        return (CHESTNUT_NULL, f"File I/O Error: File not found at path \"{path.value}\"")
    except Exception as e:
        print(f"File I/O Error: Failed to open file: {e}")
        return (CHESTNUT_NULL, f"File I/O Error: Failed to open file: {e}")

def __internal_read_file__(handle, size):
    if not isinstance(handle, ChestnutFileHandle):
        return ChestnutTuple((CHESTNUT_NULL, ChestnutError("First argument to must be a FileHandle.")))
    if not isinstance(size, ChestnutInteger):
        return ChestnutTuple((CHESTNUT_NULL, ChestnutError("Read size must be an Integer.")))

    file_object = handle.value
    if file_object.closed:
        return ChestnutTuple((CHESTNUT_NULL, ChestnutError("Attempted to read from a closed file handle.")))

    try:
        data = file_object.read(size.value)
        
        return ChestnutTuple((ChestnutString(data), CHESTNUT_NULL))
    except Exception as e:
        return ChestnutTuple((CHESTNUT_NULL, ChestnutError(f"File I/O error during read: {e}")))


def __internal_write_file__(handle, data):
    if not isinstance(handle, ChestnutFileHandle):
        return ChestnutTuple(CHESTNUT_NULL, ChestnutError("First argment must be a file handle"))
    file_object = handle.value
    if file_object.closed:
        return ChestnutTuple(CHESTNUT_NULL, ChestnutError("Write attempted to closed file handle"))
    try:
        value = data
        if isinstance(data, ChestnutAny):
            value = data.value
        written = file_object.write(value)
        return ChestnutTuple(ChestnutInteger(written), CHESTNUT_NULL)
    except Exception as e:
        return ChestnutTuple(CHESTNUT_NULL, ChestnutError(e))

def __internal_delete_file__(path):
    import os
    if not isinstance(path, ChestnutString):
        return ChestnutTuple(CHESTNUT_NULL, ChestnutError(f"Path must be a String {path.__class__.__name__} given"))
    try:
        os.remove(path.value)
    except FileNotFoundError:
        return ChestnutTuple(CHESTNUT_NULL, ChestnutError(f"File I/O Error: File not found at {path.value}"))
    except Exception as e:
        return ChestnutTuple(CHESTNUT_NULL, ChestnutError(f"File I/O Error: Failed to delete file: {e}"))
    return ChestnutTuple(ChestnutBoolean(True), CHESTNUT_NULL)

def __internal_close_file__(handle):
    if not isinstance(handle, ChestnutFileHandle):
        return ChestnutTuple((CHESTNUT_NULL, ChestnutError("Argument to close_file must be a FileHandle.")))
    return ChestnutTuple((handle.close(), CHESTNUT_NULL))

def __internal_file_exists__(path):
    if not isinstance(path, ChestnutString):
        return ChestnutTuple(CHESTNUT_NULL, ChestnutError("path needs to be String in file_exists"))
    import os
    try:
        ret = ChestnutTuple((os.path.exists(path.value), CHESTNUT_NULL))
        return ret
    except Exception as e:
        return ChestnutTuple((CHESTNUT_NULL, f"Error in file_exists: {e}"))
    
def __internal_halt__(message):
    raise RuntimeException(message)

def __internal_env_unset__(var_name):
    import os
    vname = var_name.value if isinstance(var_name, ChestnutAny) else str(var_name)
    if vname in os.environ:
        del os.environ[vname]

def __internal_env_set__(var_name, value):
    import os
    vname = var_name.value if isinstance(var_name, ChestnutAny) else str(var_name)
    v = value.value if isinstance(value, ChestnutAny) else str(value)

    if v is None:
        __internal_env_unset__(vname)

    os.environ[vname] = v

def __internal_env_get__(var_name, default=CHESTNUT_NULL):
    import os
    vname = var_name.value if isinstance(var_name, ChestnutAny) else str(var_name)
    if vname in os.environ:
        return ChestnutString(os.environ[vname])
    return default

def __internal_to_uint8__(v):
    if isinstance(v, ChestnutInteger):
        return ChestnutUInt8(v.value)

    if isinstance(v, ChestnutString):
        bytes = ChestnutList([ ChestnutUInt8(x) for x in v.value.encode("utf-8") ])
    return bytes

def __internal_to_uint16__(v):
    if isinstance(v, ChestnutInteger):
        return ChestnutUInt16(v.value)

    if isinstance(v, ChestnutString):
        return [ ChestnutUInt16(x.value) for x in __internal_to_uint16__(v) ]

def __internal_to_uint32__(v):
    if isinstance(v, ChestnutInteger):
        return ChestnutUInt32(v.value)

    if isinstance(v, ChestnutString):
        return [ ChestnutUInt32(x.value) for x in __internal_to_uint32__(v) ]

def __internal_to_uint64__(v):
    if isinstance(v, ChestnutInteger):
        return ChestnutUInt64(v.value)

    if isinstance(v, ChestnutString):
        return [ ChestnutUInt64(x.value) for x in __internal_to_uint8__(v) ]

def __internal_to_uint128__(v):
    if isinstance(v, ChestnutInteger):
        return ChestnutUInt128(v.value)

    if isinstance(v, ChestnutString):
        return [ ChestnutUInt128(x.value) for x in __internal_to_uint8__(v) ]

def __internal_from_bytes_to_string__(v):
    if isinstance(v, ChestnutInteger):
        return ChestnutString(v.value.decode("utf-8"))
    if isinstance(v, ChestnutList):
        return ChestnutString("".join([ x.value for x in v.value]))
    
def __internal_int_list_to_hex__(v):
    l = [ x.value for x in v ]
    return ''.join('{:08x}'.format(a) for a in l)

def __internal_get_bit_width__(v):
    if hasattr(v[0], "BIT_WIDTH"):
        return ChestnutInteger(v[0].BIT_WIDTH)
    return ChestnutInteger(v[0].value.bit_length())

def __internal_get_time__():
    import time
    return ChestnutInteger(time.time())

def __internal_round__(v, d=CHESTNUT_NULL):
    if d == CHESTNUT_NULL:
        return v.__class__(round(v.value))
    else:
        return v.__class__(round(v.value, d.value))

