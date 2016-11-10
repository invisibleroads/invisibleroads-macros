from invisibleroads_macros.table import normalize_key


def test_normalize_key():
    f = normalize_key
    assert f('ONETwo', separate_camel_case=True) == 'one two'
    assert f('OneTwo', separate_camel_case=True) == 'one two'
    assert f('one-two') == 'one two'
    assert f('one_two') == 'one two'
    assert f('1two', separate_letter_digit=True) == '1 two'
    assert f('one2', separate_letter_digit=True) == 'one 2'
    assert f('one--__  -_-_two   three  --__') == 'one two three'
