from invisibleroads_macros.log import format_nested_dictionary


class TestFormatNestedDictionary(object):

    def test_hide_censored_key(self):
        value_by_key = {'a': {'_x': 1, 'y': 2}}
        x = format_nested_dictionary(value_by_key, censored=True)
        assert 'a._x = 1' not in x
        assert 'a.y = 2' in x
