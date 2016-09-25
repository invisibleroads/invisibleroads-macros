import functools
import re
import shlex
import sys
from importlib import import_module
from six.moves.configparser import NoSectionError, RawConfigParser

from .iterable import merge_dictionaries


class RawCaseSensitiveConfigParser(RawConfigParser):
    optionxform = str


def load_settings(configuration_path, section_name):
    configuration = RawCaseSensitiveConfigParser()
    configuration.read(configuration_path)
    try:
        d = dict(configuration.items(section_name))
    except NoSectionError:
        d = {}
    return d


def parse_settings(settings, prefix, parse_setting=None):
    d = {}
    prefix_pattern = re.compile('^' + prefix.replace('.', r'\.'))
    if not parse_setting:
        parse_setting = parse_raw_setting
    for k, v in settings.items():
        if not k.startswith(prefix):
            continue
        d = merge_dictionaries(d, parse_setting(prefix_pattern.sub('', k), v))
    return d


def parse_raw_setting(k, v):
    return {k: v}


def resolve_attribute(attribute_spec):
    # Modified from pkg_resources.EntryPoint.resolve()
    if not attribute_spec or not hasattr(attribute_spec, 'split'):
        return attribute_spec
    module_url, attributes_string = attribute_spec.split(':')
    module = import_module(module_url)
    try:
        attribute = functools.reduce(
            getattr, attributes_string.split('.'), module)
    except AttributeError:
        raise ImportError('could not resolve attribute (%s)' % module_url)
    return attribute


def split_arguments(command_string):
    # Strip line breaks: \ for POSIX, ^ for Windows
    lines = []
    for line in command_string.splitlines():
        lines.append(line.rstrip(' \\^'))
    string = ' '.join(lines)
    # Split terms
    try:
        xs = shlex.split(string)
    except UnicodeEncodeError:
        xs = shlex.split(string.encode('utf-8'))
    return [x.strip() for x in xs]


def unicode_safely(x):
    # http://stackoverflow.com/a/23085282/192092
    if not hasattr(x, 'decode'):
        return x
    return x.decode(sys.getfilesystemencoding())
