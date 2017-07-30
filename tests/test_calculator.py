from invisibleroads_macros.calculator import digitize


def test_digitize():
    assert digitize(0.1) == 1
    assert digitize(-0.1) == -1
