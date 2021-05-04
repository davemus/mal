from operator import (
    add, sub, mul, truediv, lt, le, gt, ge
)
from printer import pr_str
from reader import read_str
from mal_types import (
    make_list, is_list, NIL, is_empty, count,
    is_iterable, make_symbol, is_symbol,
    make_atom, is_atom, deref, swap, reset,
    cons, concat, make_vector, is_vector, make_vector_vargs,
    first, rest, nth,
    is_nil, is_true, is_false, make_keyword, is_keyword,
    is_hashmap, keys, values, contains, get,
    make_hashmap_vargs, assoc, dissoc, make_string,
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
    if is_hashmap(op1) and is_hashmap(op2):
        if set(keys(op1)) != set(keys(op2)):
            return False
        return all(equal(op1[key], op2[key]) for key in keys(op1))
    return type(op1) == type(op2) and op1 == op2


def slurp(filename):
    strip_comments = lambda line: line.split(';')[0]
    with open(filename) as f:
        contents = ' '.join(strip_comments(line) for line in f if line)
    return contents


def mal_readline(prompt):
    try:
        return input(prompt)
    except EOFError:
        return NIL


def stub(*args):
    raise NotImplementedError('Stub')


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
    'read-string': read_str,
    'slurp': slurp,
    'atom': make_atom,
    'atom?': is_atom,
    'deref': deref,
    'swap!': swap,
    'reset!': reset,
    'cons': cons,
    'concat': concat,
    'vec': make_vector,
    'first': first,
    'rest': rest,
    'nth': nth,
    'nil?': is_nil,
    'true?': is_true,
    'false?': is_false,
    'symbol': make_symbol,
    'symbol?': is_symbol,
    'keyword': make_keyword,
    'keyword?': is_keyword,
    'vector': make_vector_vargs,
    'vector?': is_vector,
    'sequential?': is_iterable,
    'hash-map': make_hashmap_vargs,
    'map?': is_hashmap,
    'get': get,
    'keys': keys,
    'vals': values,
    'contains?': contains,
    'assoc': assoc,
    'dissoc': dissoc,
    'readline': mal_readline,
    '*host-language*': make_string("\"python-mal\""),
    'time-ms': stub,
    'meta': stub,
    'with-meta': stub,
    'fn?': stub,
    'string?': stub,
    'number?': stub,
    'seq': stub,
    'conj': stub,
}

namespace = {make_symbol(k): v for k, v in namespace_.items()}
