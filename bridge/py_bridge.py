def __internal_print__(*args):
    print(*args)

def __internal_length__(a):
    return len(a)

def __internal_readline__():
    return input()

def __internal_insert__(l, a, i):
    l.insert(i, a)

def __internal_remove__(l, i):
    return l.pop(i)

