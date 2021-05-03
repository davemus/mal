# atomic types
make_number = lambda str_: float(str_) if float(str_) != int(str_) else int(str_)
is_number = lambda entity: isinstance(entity, (int, float))

def make_string(str_):
    return (
        str_[1:-1]
        # that hack I saw in impl/python. I was desperate to complete step4
        # cause I was stopped on it for 5+ days. I have only 7 incomplete tests so far
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
is_list = lambda entity: isinstance(entity, list)

make_vector = tuple
is_vector = lambda entity: isinstance(entity, tuple)

make_hashmap = lambda iterable: dict(zip(iterable[0::2], iterable[1::2]))
make_hashmap_from_pydict = lambda x: x
is_hashmap = lambda entity: isinstance(entity, dict)

NIL = None
is_nil = lambda entity: entity is NIL

TRUE = True
FALSE = False
is_bool = lambda entity: isinstance(entity, bool)

is_function = lambda entity: callable(entity)


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
