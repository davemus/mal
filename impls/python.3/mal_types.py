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
is_hashmap = lambda entity: isinstance(entity, dict)
