from invisibleroads_macros.configuration import get_list


def test_get_list():
    f = get_list
    assert f('one two') == ['one', 'two']
    assert f(['one', 'two']) == ['one', 'two']
