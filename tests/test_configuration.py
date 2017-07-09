from invisibleroads_macros.configuration import (
    parse_list, parse_second_count, set_default)
from pytest import raises


def test_parse_list():
    f = parse_list
    assert f('one two') == ['one', 'two']
    assert f(['one', 'two']) == ['one', 'two']


def test_parse_second_count():
    f = parse_second_count
    with raises(ValueError):
        f(3.5)
    with raises(ValueError):
        f('3')
    with raises(ValueError):
        f('3x')
    assert f('3h') == 3 * 60 * 60
    assert f('3m') == 3 * 60
    assert f('3s') == 3
    assert f(3) == 3


def test_set_default():
    f = set_default
    assert f({}, 'x') is None
    assert f({}, 'x', 1) == 1
    assert f({'x': '2'}, 'x', 1, int) == 2
