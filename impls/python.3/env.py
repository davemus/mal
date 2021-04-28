from mal_types import (
    make_symbol, make_list
)


VARIADIC_ASSIGNMENT_SYMBOL = make_symbol('&')


class Env:
    def __init__(self, outer=None, binds=[], exprs=[]):
        self._scope = {}
        self._outer = outer
        if (
            len(binds) != len(exprs)
            and VARIADIC_ASSIGNMENT_SYMBOL not in binds
        ):
            raise ValueError
        for counter in range(len(exprs)):
            if binds[counter] == VARIADIC_ASSIGNMENT_SYMBOL:
                self.set(binds[counter + 1], make_list(exprs[counter:]))
                return
            self.set(binds[counter], exprs[counter])

    def set(self, name, value):
        self._scope[name] = value

    def find(self, name):
        if name in self._scope:
            return self
        elif self._outer is not None:
            return self._outer.find(name)
        return None

    def get(self, name):
        env = self.find(name)
        if env is None:
            raise RuntimeError(f"'{name}' not found")
        return env._scope[name]

    def __str__(self):
        str_repr = f'Definitions on this level: {tuple(self._scope)}'
        if self._outer is None:
            return str_repr
        return str_repr + '    ' + str(self._outer)
