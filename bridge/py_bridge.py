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

