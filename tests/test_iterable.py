from invisibleroads_macros.iterable import set_default


def test_set_default():
    f = set_default
    assert f({}, 'x') is None
    assert f({}, 'x', 1) == 1
    assert f({'x': '2'}, 'x', 1, int) == 2
