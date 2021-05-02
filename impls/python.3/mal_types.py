# atomic types
make_number = lambda str_: float(str_) if float(str_) != int(str_) else int(str_)
is_number = lambda entity: isinstance(entity, (int, float))

make_string = str
is_string = lambda entity: isinstance(entity, str) and entity.startswith('"')

make_keyword = lambda str_: u"\u029e" + str(str_)
is_keyword = lambda entity: isinstance(entity, str) and entity.startswith(u"\u029e")

make_symbol = str
is_symbol = lambda entity: isinstance(entity, str) and not any([is_string(entity), is_keyword(entity)])

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
