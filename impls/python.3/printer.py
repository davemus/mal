from mal_types import (
    is_number,
    is_symbol,
    is_list,
    is_vector,
    is_hashmap,
    is_nil,
    is_bool,
    TRUE,
    FALSE,
    is_function,
)


def pr_str(entity, print_readably=True):
    if is_function(entity):
        return '#function'
    elif is_nil(entity):
        return 'nil'
    elif is_bool(entity):
        return {
            TRUE: 'true',
            FALSE: 'false',
        }[entity]
    elif is_number(entity):
        return str(entity)
    elif is_symbol(entity):
        return str(entity)
    elif is_list(entity):
        return '(' + ' '.join(pr_str(inner) for inner in entity) + ')'
    elif is_vector(entity):
        return '[' + ' '.join(pr_str(inner) for inner in entity) + ']'
    elif is_hashmap(entity):
        return (
            '{'
            + ' '.join(f'{pr_str(k)} {pr_str(v)}' for k, v in entity.items())
            + '}'
        )
    raise RuntimeError(f'pr_str: unknown type {type(entity)}')
