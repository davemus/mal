from operator import (
    add, sub, mul, truediv, lt, le, gt, ge
)
from printer import pr_str
from mal_types import (
    make_list, is_list, first, NIL, is_empty, count,
    is_iterable, TRUE, FALSE,
)


def prn(*args):
    first_arg_as_str = pr_str(first(args), True)
    print(first_arg_as_str)
    return NIL


def equal(op1, op2):
    if is_iterable(op1):  # list and vector are equal in tests =(
        if count(op1) != count(op2):
            return False
        return all(
            equal(el1, el2) for (el1, el2) in zip(op1, op2)
        )
    return type(op1) == type(op2) and op1 == op2


namespace = {
    '+': add,
    '-': sub,
    '*': mul,
    '/': truediv,
    '<': lt,
    '<=': le,
    '>': gt,
    '>=': ge,
    '=': equal,
    'list': lambda *args: make_list(args),
    'list?': is_list,
    'prn': prn,
    'empty?': is_empty,
    'count': count,
}
