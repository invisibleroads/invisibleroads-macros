import functools
import re
import shlex
import sys
from collections import defaultdict
from importlib import import_module
from six.moves.configparser import RawConfigParser


class RawCaseSensitiveConfigParser(RawConfigParser):
    optionxform = str


def get_interpretation_by_name(settings, prefix, interpret_setting):
    interpretation_by_name = defaultdict(dict)
    pattern_key = re.compile(prefix.replace('.', r'\.') + r'(.*)\.(.*)')
    for key, value in settings.items():
        try:
            name, attribute = pattern_key.match(key).groups()
        except AttributeError:
            continue
        interpretation = interpretation_by_name[name]
        interpretation.update(interpret_setting(attribute, value))
    return interpretation_by_name


def resolve_attribute(attribute_spec):
    # Modified from pkg_resources.EntryPoint.resolve()
    module_name, attributes_string = attribute_spec.split(':')
    attributes = attributes_string.split('.')
    module = import_module(module_name)
    try:
        attribute = functools.reduce(getattr, attributes, module)
    except AttributeError as e:
        raise ImportError(e)
    return attribute


def split_arguments(x):
    try:
        return shlex.split(x)
    except UnicodeEncodeError:
        return shlex.split(x.encode('utf-8'))


def unicode_safely(x):
    # http://stackoverflow.com/a/23085282/192092
    if not hasattr(x, 'decode'):
        return x
    return x.decode(sys.getfilesystemencoding())
