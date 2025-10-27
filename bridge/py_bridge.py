from chestnut_type import *
from error import *
def __internal_print__(*args):
    print(*args)

def __internal_length__(a):
    return ChestnutInteger(len(a))

def __internal_readline__():
    return ChestnutString(input())

def __internal_insert__(l, a, i):
    index = i
    if isinstance(i, ChestnutInteger):
        index = i.value
    l.insert(index, a)

def __internal_remove__(l, i):
    index = i
    if isinstance(i, ChestnutInteger):
        index = i.value
    return l.pop(index)

def __internal_type__(o):
    if isinstance(o, ChestnutAny):
        return f"{o.gettype()}"
    return str("Python " + type(o))

def __internal_open_file__(path, mode):
    if not isinstance(path, ChestnutString) or not isinstance(mode, ChestnutString):
        raise TypeException("File path and mode must be Strings.")
    
    try:
        file_object = open(path.value, mode.value)
        return ChestnutFileHandle(file_object)
    except FileNotFoundError:
        print(f"File I/O Error: File not found at path '{path.value}'")
        return ChestnutNull(None)
    except Exception as e:
        print(f"File I/O Error: Failed to open file: {e}")
        return ChestnutNull(None)

def __internal_read_file__(handle, size):
    if not isinstance(handle, ChestnutFileHandle):
        raise TypeException("First argument to read_file must be a FileHandle.")
    if not isinstance(size, ChestnutInteger):
        raise TypeException("Read size must be an Integer.")

    file_object = handle.value
    if file_object.closed:
        print("File I/O Warning: Attempted to read from a closed file handle.")
        return ChestnutNull(None)

    try:
        data = file_object.read(size.value)
        
        return ChestnutString(data)
    except Exception as e:
        print(f"File I/O Error during read: {e}")
        return ChestnutNull(None)

def __internal_close_file__(handle):
    if not isinstance(handle, ChestnutFileHandle):
        raise TypeException("Argument to close_file must be a FileHandle.")
    
    return handle.close()
