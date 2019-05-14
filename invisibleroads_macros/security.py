from random import SystemRandom
from string import ascii_letters, digits


ALPHABET = digits + ascii_letters
RANDOM = SystemRandom()


def make_random_string(length, alphabet=ALPHABET):
    # Adapted from invisibleroads-macros
    return ''.join(RANDOM.choice(alphabet) for _ in range(length))
