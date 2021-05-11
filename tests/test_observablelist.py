from typing import MutableSequence

from qtwidgets.observablelist import observablelist


def change_list(m: MutableSequence):
    m.append('append')
    m[-1] = 'replace last'
    m[3:5] = ('slice', 'value', 'tuple')
    m.extend('extend func')
    m += ['a', 'new', 'array', 'with', '+']
    del m[4:10]
    m.pop()
    m.remove(1)


if __name__ == '__main__':
    m = observablelist(range(10))
    m.add_after_change_obervers(lambda x: print(x))
    l = list(range(10))

    change_list(l)
    change_list(m)

    print(l)
    print(m)
    assert l == m

    l.reverse()
    m.reverse()

    print(l)
    print(m)
    assert l == m

    l.clear()
    m.clear()

    print(l)
    print(m)
    assert l == m
