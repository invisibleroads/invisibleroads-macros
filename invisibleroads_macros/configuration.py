import codecs
import functools
import re
import shlex
import sys
from argparse import ArgumentError, ArgumentParser
from collections import OrderedDict
from importlib import import_module
from os.path import dirname, expanduser, isabs, join, relpath
from six.moves.configparser import NoSectionError, RawConfigParser

from .disk import expand_path, resolve_relative_path
from .iterable import merge_dictionaries
from .log import format_summary


SECTION_TEMPLATE = '[%s]\n%s\n'


class StoicArgumentParser(ArgumentParser):

    def add_argument(self, *args, **kw):
        try:
            return super(StoicArgumentParser, self).add_argument(*args, **kw)
        except ArgumentError:
            pass


class TerseArgumentParser(StoicArgumentParser):

    def add(self, argument_name, *args, **kw):
        d = {}
        if argument_name.endswith('_path'):
            d['metavar'] = 'PATH'
        elif '_as_percent_of_' in argument_name:
            d['metavar'] = 'FLOAT'
            d['type'] = float
        elif argument_name.endswith('_year'):
            d['metavar'] = 'YEAR'
            d['type'] = int
        elif argument_name.endswith('_in_years'):
            d['metavar'] = 'INTEGER'
            d['type'] = int
        d.update(kw)
        self.add_argument('--' + argument_name, *args, **d)


class RawCaseSensitiveConfigParser(RawConfigParser):
    optionxform = str


def load_relative_settings(configuration_path, section_name):
    settings = OrderedDict()
    configuration_folder = dirname(expand_path(configuration_path))
    for k, v in load_settings(configuration_path, section_name).items():
        if k.endswith('_path') or k.endswith('_folder'):
            v = resolve_relative_path(expanduser(v), configuration_folder)
        settings[k] = v
    return settings


def load_settings(configuration_path, section_name):
    configuration = RawCaseSensitiveConfigParser()
    configuration.read(configuration_path)
    try:
        items = configuration.items(section_name)
    except NoSectionError:
        items = []
    return OrderedDict(items)


def save_settings(configuration_path, settings_by_section_name):
    configuration_file = codecs.open(configuration_path, 'w', encoding='utf-8')
    configuration_file.write(format_settings(settings_by_section_name) + '\n')
    return configuration_path


def format_settings(settings_by_section_name):
    configuration_parts = []
    for section_name, settings in settings_by_section_name.items():
        configuration_parts.append(SECTION_TEMPLATE % (
            section_name, format_summary(settings)))
    return '\n'.join(configuration_parts).strip()


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


def make_absolute_paths(d, folder):
    d = OrderedDict(d)
    for k, v in d.items():
        if hasattr(v, 'items'):
            v = make_absolute_paths(v, folder)
        elif is_path_key(k) and v:
            v = expanduser(v)
            if not isabs(v):
                v = join(folder, v)
        d[k] = v
    return d


def make_relative_paths(d, folder):
    folder = expanduser(folder)
    d = OrderedDict(d)
    for k, v in d.items():
        if hasattr(v, 'items'):
            v = make_relative_paths(v, folder)
        elif is_path_key(k):
            v = expanduser(v)
            if not isabs(v):
                continue
            v = relpath(v, folder)
            if v.startswith('.'):
                continue
        d[k] = v
    return d


def is_path_key(k):
    return k.endswith('_path') or k.endswith('_folder')
