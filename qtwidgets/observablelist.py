from typing import Callable, Iterable, Any, List

Observer = Callable[[Any], None]


class observablelist(list):
    def __init__(self, items: Iterable = None):
        super().__init__(items or [])
        self.before_observers: List[Observer] = []
        self.after_observers: List[Observer] = []

    def add_before_change_observer(self, observer: Observer):
        self.before_observers.append(observer)

    def add_after_change_obervers(self, observer: Observer):
        self.after_observers.append(observer)

    def __delitem__(self, *args, **kwargs):
        self.__before('__delitem__', *args, **kwargs)
        super().__delitem__(*args, **kwargs)
        self.__after('__delitem__', *args, **kwargs)

    def __setitem__(self, *args, **kwargs):
        self.__before('__setitem__', *args, **kwargs)
        super().__setitem__(*args, **kwargs)
        self.__after('__setitem__', *args, **kwargs)

    def __iadd__(self, *args, **kwargs):
        self.__before('__iadd__', *args, **kwargs)
        super().__iadd__(*args, **kwargs)
        self.__after('__iadd__', *args, **kwargs)
        return self

    def append(self, *args, **kwargs):
        self.__before('append', *args, **kwargs)
        super().append(*args, **kwargs)
        self.__after('append', *args, **kwargs)

    def extend(self, *args, **kwargs):
        self.__before('extend', *args, **kwargs)
        super().extend(*args, **kwargs)
        self.__after('extend', *args, **kwargs)

    def remove(self, *args, **kwargs):
        self.__before('remove', *args, **kwargs)
        super().remove(*args, **kwargs)
        self.__after('remove', *args, **kwargs)

    def pop(self, *args, **kwargs):
        self.__before('pop', *args, **kwargs)
        res = super().pop(*args, **kwargs)
        self.__after('pop', *args, **kwargs)
        return res

    def clear(self):
        self.__before('clear')
        res = super().clear()
        self.__after('clear')
        return res

    def reverse(self):
        self.__before('reverse')
        res = super().reverse()
        self.__after('reverse')
        return res

    def __before(self, name, *args, **kwargs):
        self.__propagate(self.before_observers, name, *args, **kwargs)

    def __after(self, name, *args, **kwargs):
        self.__propagate(self.after_observers, name, *args, **kwargs)

    @staticmethod
    def __propagate(observers: List[Observer], name, *args, **kwargs):
        for observer in observers:
            observer({
                'name': name,
                'args': args,
                'kwargs': kwargs
            })
