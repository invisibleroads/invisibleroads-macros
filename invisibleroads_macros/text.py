import re


WHITESPACE_PATTERN = re.compile(r'\s+', re.MULTILINE)
PUNCTUATION_PATTERN = re.compile(r'[^a-zA-Z\s]+')


def lower_first_character(x):
    # http://stackoverflow.com/a/3847369/192092
    return x[:1].lower() + x[1:] if x else ''


def parse_words(x):
    return x.replace(',', ' ').split()


def strip_whitespace(string):
    return WHITESPACE_PATTERN.sub('', string)


def compact_whitespace(string):
    return WHITESPACE_PATTERN.sub(' ', string).strip()


def remove_punctuation(string):
    return compact_whitespace(PUNCTUATION_PATTERN.sub(' ', string))
