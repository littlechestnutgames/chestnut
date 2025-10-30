from chestnut_type import *
from error import *
def __internal_print__(*args):
    print(*args)
    return ChestnutNull(None)

def __internal_length__(a):
    return ChestnutInteger(len(a))

def __internal_readline__():
    return ChestnutString(input())

def __internal_insert__(l, a, i):
    index = i
    if isinstance(i, ChestnutInteger):
        index = i.value
    l.insert(index, a)
    return ChestnutNull(None)

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
        return (ChestnutNull(None), ChestnutError("File path and mode must be strings"))
    
    try:
        file_object = open(path.value, mode.value)
        return (ChestnutFileHandle(file_object), ChestnutNull(None))
    except FileNotFoundError:
        return (ChestnutNull(None), f"File I/O Error: File not found at path \"{path.value}\"")
    except Exception as e:
        print(f"File I/O Error: Failed to open file: {e}")
        return (ChestnutNull(None), f"File I/O Error: Failed to open file: {e}")

def __internal_read_file__(handle, size):
    if not isinstance(handle, ChestnutFileHandle):
        return ChestnutTuple((ChestnutNull(None), ChestnutError("First argument to must be a FileHandle.")))
    if not isinstance(size, ChestnutInteger):
        return ChestnutTuple((ChestnutNull(None), ChestnutError("Read size must be an Integer.")))

    file_object = handle.value
    if file_object.closed:
        return ChestnutTuple((ChestnutNull(None), ChestnutError("Attempted to read from a closed file handle.")))

    try:
        data = file_object.read(size.value)
        
        return ChestnutTuple((ChestnutString(data), ChestnutNull(None)))
    except Exception as e:
        return ChestnutTuple((ChestnutNull(None), ChestnutError(f"File I/O error during read: {e}")))

def __internal_close_file__(handle):
    if not isinstance(handle, ChestnutFileHandle):
        return ChestnutTuple((ChestnutNull(None), ChestnutError("Argument to close_file must be a FileHandle.")))
    return ChestnutTuple((handle.close(), ChestnutNull(None)))

def __internal_halt__(message):
    raise RuntimeException(message)
