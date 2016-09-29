import re

from .text import compact_whitespace


UPPER_LOWER_PATTERN = re.compile(r'(.)([A-Z][a-z]+)')
LOWER_UPPER_PATTERN = re.compile(r'([a-z0-9])([A-Z])')
DIGIT_LETTER_PATTERN = re.compile(r'([0-9])([a-z])')
LETTER_DIGIT_PATTERN = re.compile(r'([a-z])([0-9])')


def duplicate_selected_column_names(selected_column_names, column_names):
    suffix = '*'
    while set(column_names).intersection(
            x + suffix for x in selected_column_names):
        suffix += '*'
    return list(column_names) + [x + suffix for x in selected_column_names]


def normalize_column_name(column_name, word_separator=' '):
    """
    Normalize name variations, using a variation of the method described in
    http://stackoverflow.com/a/1176023/192092

    ONETwo   one two
    OneTwo   one two
    one-two  one two
    one_two  one two
    1two     1 two
    one2     one 2
    """
    s = UPPER_LOWER_PATTERN.sub(r'\1 \2', column_name)
    s = LOWER_UPPER_PATTERN.sub(r'\1 \2', s).lower()
    s = DIGIT_LETTER_PATTERN.sub(r'\1 \2', s)
    s = LETTER_DIGIT_PATTERN.sub(r'\1 \2', s)
    word_separators = ['-', '_', ' ']
    if word_separator not in word_separators:
        word_separators.append(word_separator)
    word_separator_expression = '[' + ''.join(word_separators) + ']'
    word_separator_pattern = re.compile(word_separator_expression)
    s = word_separator_pattern.sub(' ', s)
    s = compact_whitespace(s)
    return s.replace(' ', word_separator)
