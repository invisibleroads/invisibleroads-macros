import random
import string


try:
    ALPHABET = string.digits + string.letters
except AttributeError:
    ALPHABET = string.digits + string.ascii_letters


def make_random_string(
        length, with_punctuation=False, with_spaces=False, alphabet=ALPHABET):
    if with_punctuation:
        alphabet += string.punctuation
    if with_spaces:
        alphabet += ' '
    return ''.join(random.choice(alphabet) for x in range(length))
