from invisibleroads_macros.url import format_url


def test_format_url():
    f = format_url
    assert f() == 'http://localhost'
    assert f(port=80) == 'http://localhost'
    assert f(port=8000) == 'http://localhost:8000'
    assert f('11.22.33.44', port=4000) == 'http://11.22.33.44:4000'
    assert f('https://11.22.33.44', scheme='http') == 'http://11.22.33.44'
