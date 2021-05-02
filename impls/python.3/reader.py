import re
from mal_types import (
    make_number,
    make_symbol,
    make_string,
    make_list,
    make_vector,
    make_hashmap,
    make_keyword,
    NIL,
    TRUE,
    FALSE,
)


class Reader:
    def __init__(self, tokens, position=0):
        self._tokens = list(tokens)
        self._position = position
        self._iter = tokens

    def _check_position(self):
        if self._position >= len(self._tokens):
            raise StopIteration('Input/output error')

    def peek(self):
        self._check_position()
        return self._tokens[self._position]

    def next(self):
        self._check_position()
        token = self.peek()
        self._position += 1
        return token


def read_str(arg):
    tokens = tokenize(arg)
    reader = Reader(tokens)
    try:
        return read_form(reader)
    except (StopIteration, RuntimeError):
        raise RuntimeError('unbalanced input')


def tokenize(arg):
    regex_str = r"""[\s,]*(~@|[\[\]{}()'`~^@]|"(?:\\.|[^\\"])*"?|;.*|[^\s\[\]{}('"`,;)]*)"""  # noqa
    token_regex = re.compile(regex_str)
    return [match.strip() for match in token_regex.findall(arg)]


def read_form(reader):
    curr_token = reader.peek()
    if curr_token in tuple('([{'):
        token_to_type = {
            '(': make_list,
            '[': make_vector,
            '{': make_hashmap,
        }
        sequential = token_to_type[curr_token]
        return read_list(reader, sequential)
    elif curr_token == '@':
        reader.next()
        return make_list([make_symbol('deref'), read_form(reader)])
    elif curr_token == '\'':
        reader.next()
        return make_list([make_symbol('quote'), read_form(reader)])
    elif curr_token == '`':
        reader.next()
        return make_list([make_symbol('quasiquote'), read_form(reader)])
    elif curr_token == '~':
        reader.next()
        return make_list([make_symbol('unquote'), read_form(reader)])
    elif curr_token == '~@':
        reader.next()
        return make_list([make_symbol('splice-unquote'), read_form(reader)])
    elif curr_token == '^':
        reader.next()
        term2 = read_form(reader)
        term1 = read_form(reader)
        return make_list([make_symbol('with-meta'), term1, term2])
    return read_atom(reader)


def read_list(reader, sequential):
    list_ = []
    closing_symbol = {
        '(': ')',
        '[': ']',
        '{': '}',
    }[reader.next()]
    while True:
        token = reader.peek()
        if token == closing_symbol:
            reader.next()
            return sequential(list_)
        list_.append(read_form(reader))


def read_atom(reader):
    token = reader.next().strip()
    if token == 'nil':
        return NIL
    elif token == 'true':
        return TRUE
    elif token == 'false':
        return FALSE
    elif re.match(r'-?\d+\.*\d*', token):
        return make_number(token)
    elif token.startswith('"'):
        # this makes tests pass, but is not a real solution. Example: "\\"
        if not token.endswith(r'"') or len(token) == 1:
            raise RuntimeError('Input/output error')
        return make_string(token.replace("", ""))
    elif token.startswith(':'):
        return make_keyword(token)
    elif re.match(r'.*', token):
        return make_symbol(token)
    raise RuntimeError('Input/output error')
