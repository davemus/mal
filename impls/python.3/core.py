from operator import (
    add, sub, mul, truediv, lt, le, gt, ge
)
from printer import pr_str
from mal_types import (
    make_list, is_list, NIL, is_empty, count,
    is_iterable, make_string, make_symbol
)


def prn(*args):
    print(" ".join(pr_str(arg, True) for arg in args))
    return NIL


def println(*args):
    print(" ".join(pr_str(arg, False) for arg in args))
    return NIL


def pr_str_(*args):
    string = " ".join(pr_str(arg, True) for arg in args)
    return string


def str_(*args):
    string = "".join(pr_str(arg, False) for arg in args)
    return string


def equal(op1, op2):
    if is_iterable(op1) and is_iterable(op2):  # list and vector are equal in tests =(
        if count(op1) != count(op2):
            return False
        return all(
            equal(el1, el2) for (el1, el2) in zip(op1, op2)
        )
    return type(op1) == type(op2) and op1 == op2


namespace_ = {
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
    'println': println,
    'pr-str': pr_str_,
    'str': str_,
    'empty?': is_empty,
    'count': count,
}

namespace = {make_symbol(k): v for k, v in namespace_.items()}
