from invisibleroads_macros.text import (
    compact_whitespace, has_whitespace, parse_words, cut_and_strip,
    remove_punctuation, strip_whitespace)


def test_compact_whitespace():
    assert compact_whitespace('  x  y  z  ') == 'x y z'


def test_cut_and_strip():
    assert cut_and_strip(' x : y ', ':') == ('x', 'y')


def test_has_whitespace():
    assert has_whitespace('whee') is False
    assert has_whitespace('whee\n') is True
    assert has_whitespace('whee\t') is True


def test_parse_words():
    assert parse_words('one, two three') == ['one', 'two', 'three']


def test_remove_punctuation():
    assert remove_punctuation('yes & no!') == 'yes no'


def test_strip_whitespace():
    assert strip_whitespace('  x  y  z  ') == 'xyz'
