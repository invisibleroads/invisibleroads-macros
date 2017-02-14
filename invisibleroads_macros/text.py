import re


WHITESPACE_PATTERN = re.compile(r'\s+', re.MULTILINE)
PUNCTUATION_PATTERN = re.compile(r'[^a-zA-Z\s]+')


def has_whitespace(string):
    return WHITESPACE_PATTERN.search(string) is not None


def compact_whitespace(string):
    return WHITESPACE_PATTERN.sub(' ', string).strip()


def strip_whitespace(string):
    return WHITESPACE_PATTERN.sub('', string)


def remove_punctuation(string):
    return compact_whitespace(PUNCTUATION_PATTERN.sub(' ', string))


def parse_words(x):
    return x.replace(',', ' ').split()
