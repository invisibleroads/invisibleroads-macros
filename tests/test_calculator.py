from invisibleroads_macros.calculator import get_int


def test_get_int():
    assert get_int(0.1) == 1
    assert get_int(-0.1) == -1
