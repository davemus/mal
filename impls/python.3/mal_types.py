# atomic types
make_number = lambda str_: float(str_) if float(str_) != int(str_) else int(str_)
is_number = lambda entity: isinstance(entity, (int, float))
make_symbol = lambda str_: str(str_)
# TODO: add way to distinguish symbol and string
is_symbol = lambda entity: isinstance(entity, str)
make_string = str
is_string = lambda entity: isinstance(entity, str)

# compound types
make_list = list
is_list = lambda entity: isinstance(entity, list)
make_vector = tuple
is_vector = lambda entity: isinstance(entity, tuple)

make_hashmap = lambda iterable: dict(zip(iterable[0::2], iterable[1::2]))
make_hashmap_from_pydict = lambda x: x
is_hashmap = lambda entity: isinstance(entity, dict)

NIL = 'nil'
is_nil = lambda entity: entity == NIL


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
    if is_iterable(entity):
        if entity:
            return entity[0]
        return NIL
    raise TypeError


def rest(entity):
    if is_iterable(entity):
        if entity:
            return list(entity[1:])
        return []
    raise TypeError
