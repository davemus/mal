from collections import namedtuple

# atomic types
make_number = lambda str_: float(str_) if float(str_) != int(str_) else int(str_)
is_number = lambda entity: isinstance(entity, (int, float))

def make_string(str_):
    return (
        str_[1:-1]
        .replace('\\\\', u'\u029e')
        .replace('\\n', '\n')
        .replace('\\"', '"')
        .replace(u'\u029e', '\\')
    )
is_string = lambda entity: isinstance(entity, str)

make_keyword = lambda str_: u"\u029e" + str(str_)
is_keyword = lambda entity: isinstance(entity, str) and entity.startswith(u"\u029e")

make_symbol = lambda str_: bytes(str_, encoding='utf-8')
is_symbol = lambda entity: isinstance(entity, bytes)

# compound types
make_list = list
is_list = lambda entity: isinstance(entity, list) and not is_atom(entity)

make_vector = tuple
is_vector = lambda entity: isinstance(entity, tuple) and not isinstance(entity, function)

make_hashmap = lambda iterable: dict(zip(iterable[0::2], iterable[1::2]))
make_hashmap_from_pydict = lambda x: x
is_hashmap = lambda entity: isinstance(entity, dict)

NIL = None
is_nil = lambda entity: entity is NIL

TRUE = True
FALSE = False
is_bool = lambda entity: isinstance(entity, bool)

function = namedtuple('MalFunction', 'ast params env fn')
make_function = function
is_mal_function = lambda entity: isinstance(entity, function)
is_function = lambda entity: callable(entity) or is_mal_function(entity)

_atom_mark = 'atom'
atom = lambda value: make_list([_atom_mark, value])
make_atom = atom
is_atom = lambda entity: isinstance(entity, list) and len(entity) == 2 and entity[0] == _atom_mark


def deref(entity):
    if is_atom(entity):
        return entity[1]
    return NIL


def reset(entity, value):
    if is_atom(entity):
        entity[1] = value
        return value
    return NIL


def swap(entity, fn, *args):
    if not is_atom(entity):
        raise TypeError('swap! first argument should be atom')
    if is_mal_function(fn):
        fn = fn.fn
    new_value = fn(entity[1], *args)
    entity[1] = new_value
    return new_value


def items(entity):
    if is_hashmap(entity):
        return entity.items()
    raise TypeError


is_iterable = lambda entity: any(is_a(entity) for is_a in (is_list, is_vector))


def is_empty(entity):
    if is_iterable(entity):
        return not entity
    raise TypeError


def iterate(entity):
    if is_iterable(entity):
        return entity
    raise TypeError


def first(entity):
    if is_iterable(entity) and entity:
        return entity[0]
    return NIL


def rest(entity):
    if is_iterable(entity) and entity:
        return list(entity[1:])
    return []


def count(entity):
    if is_iterable(entity):
        return len(entity)
    return 0
