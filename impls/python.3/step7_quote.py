import argparse
import mal_readline  # noqa: side effect import
from reader import read_str
from printer import pr_str
from mal_types import (
    is_vector, make_vector,
    is_hashmap, make_hashmap_from_pydict, items,
    is_list, make_list, is_empty,
    is_symbol, make_symbol,
    first, rest, FALSE, is_nil, is_bool,
    make_function, is_mal_function
)
from env import Env
from core import namespace

# setup env step 1
repl_env = Env()
for symbol, value in namespace.items():
    repl_env.set(symbol, value)


def eval_ast(ast, env):
    if is_vector(ast):
        return make_vector(EVAL(elem, env) for elem in ast)
    if is_hashmap(ast):
        return make_hashmap_from_pydict(
            {key: EVAL(value, env) for key, value in items(ast)}
        )
    if is_symbol(ast):
        return env.get(ast)
    elif is_list(ast):
        return make_list(EVAL(elem, env) for elem in ast)
    else:
        return ast


def READ(str_):
    """
    Make mal instructions from string.
    """
    return read_str(str_)


def EVAL(ast, env):
    """
    Evaluate set of mal instructions.
    """
    while True:
        if not is_list(ast):
            return eval_ast(ast, env)
        elif is_empty(ast):
            return ast

        elif first(ast) == make_symbol('def!'):
            try:
                operands = rest(ast)
                symbol = first(operands)
                value = EVAL(first(rest(operands)), env)
            except ValueError:
                raise RuntimeError('def! syntax is (def! /symbol/ /value/)')
            env.set(symbol, value)
            return value

        elif first(ast) == make_symbol('let*'):
            let_error = RuntimeError('let* syntax is (let* /list_of definitions/ /list_of_instructions/)')  # noqa
            new_env = Env(env)
            try:
                operands = rest(ast)
                definitions, instructions = operands
            except Exception:
                raise let_error
            if len(definitions) % 2 != 0:
                raise let_error
            symbol_value_pairs = list(zip(
                definitions[0::2],
                definitions[1::2],
            ))
            for symb, value in symbol_value_pairs:
                new_env.set(symb, EVAL(value, new_env))
            ast = instructions
            env = new_env
            continue

        elif first(ast) == make_symbol('if'):
            elements = rest(ast)
            condition = first(elements)
            true_branch = first(rest(elements))
            false_branch = first(rest(rest(elements)))
            condition = EVAL(condition, env)
            # empty lists, strings and 0 are 'truthy', only false and nil are 'falsy'
            if is_nil(condition) or is_bool(condition) and condition == FALSE:
                ast = false_branch
            else:
                ast = true_branch
            continue

        elif first(ast) == make_symbol('fn*'):
            try:
                op, binds, body = ast
            except ValueError:
                raise RuntimeError('fn* syntax us (fn* /arguments/ /function_body/)')  # noqa

            def closure(*arguments):
                try:
                    new_env = Env(outer=env, binds=binds, exprs=arguments)
                except ValueError:
                    raise RuntimeError(
                        'Error: function is called with wrong number of parameters'
                        f'expected: {len(binds)}, actual: {len(arguments)}'
                    )
                return EVAL(body, new_env)

            return make_function(body, binds, env, closure)

        elif first(ast) == make_symbol('do'):
            op, *exprs = ast
            for expr in exprs[:-1]:
                EVAL(expr, env)
            ast = exprs[-1]
            continue

        # quoting element
        elif ast[0] == make_symbol('quote'):
            return ast[1]

        elif ast[0] == make_symbol('quasiquote'):
            ast = quasiquote(ast[1])
            continue

        func, *args = eval_ast(ast, env)
        if not is_mal_function(func):
            # core function
            return func(*args)
        ast = func.ast
        env = Env(func.env, func.params, args)


def PRINT(mal_type):
    """
    Convert result of mal instructions into string representation.
    """
    return pr_str(mal_type)


def eval_(ast):
    return EVAL(ast, repl_env)


def quasiquote(ast):
    if is_list(ast):
        if is_empty(ast):
            return ast
        if ast[0] == make_symbol('unquote'):
            return ast[1]
        else:
            processed = []
            for elt in ast[::-1]:
                if is_list(elt) and not is_empty(elt) and elt[0] == make_symbol('splice-unquote'):
                    processed = [make_symbol('concat'), elt[1], processed]
                else:
                    processed = [make_symbol('cons'), quasiquote(elt), processed]
            return make_list(processed)
    elif is_vector(ast):
        return make_list([make_symbol('vec'), *ast])
    elif is_symbol(ast) or is_hashmap(ast):
        return make_list([make_symbol('quote'), ast])
    return ast


def rep(arg):
    return PRINT(EVAL(READ(arg), repl_env))


# setup env step 2
repl_env.set(make_symbol('eval'), eval_)
rep("(def! not (fn* (a) (if a false true)))")
rep("""(def! load-file (fn* (f) (eval (read-string (str "(do " (slurp f) "\nnil)")))))""")

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--interactive', action='store_true')
parser.add_argument('filename', nargs='?', help='Filename to be executed')
parser.add_argument('prog_args', nargs='*', help='Arguments passed to program')
args = parser.parse_args()


if __name__ == '__main__':
    arg_to_str = lambda arg: f'"{arg}"'
    rep(f'(def! *ARGV* {"(list " +  " ".join(arg_to_str(arg) for arg in args.prog_args) + ")" })')
    if args.filename is not None:
        rep(f'(def! *FILENAME* "{args.filename}")')
        rep('(load-file *FILENAME*)')
        if not args.interactive:
            exit(0)
    while True:
        inp = input('user> ')
        try:
            res = rep(inp)
        except Exception as e:
            print(e)
        else:
            print(res)
