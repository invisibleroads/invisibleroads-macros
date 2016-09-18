import fnmatch
import re
import tarfile
from contextlib import contextmanager
from os import chdir, getcwd, makedirs, remove, walk
from os.path import (
    abspath, basename, dirname, join, normpath, realpath, relpath, sep,
    splitext)
from pathlib import Path
from shutil import copytree, rmtree
from tempfile import mkdtemp, mkstemp
from zipfile import ZipFile, ZIP_DEFLATED


def make_folder(folder):
    'Make sure a folder exists without raising an exception'
    try:
        makedirs(folder)
    except OSError:
        pass
    return folder


def clean_folder(folder):
    'Remove folder contents but keep folder'
    remove_safely(folder)
    return make_folder(folder)


def replace_folder(target_folder, source_folder):
    'Replace target_folder with source_folder'
    remove_safely(target_folder)
    copytree(source_folder, target_folder)
    return target_folder


def remove_safely(path):
    'Make sure a file or folder does not exist without raising an exception'
    try:
        rmtree(path)
    except OSError:
        try:
            remove(path)
        except OSError:
            pass
    return path


def make_link(source_path, target_path):
    'Create symbolic link at target_path pointing to source_path'
    from os import symlink  # Undefined in Windows
    make_folder(dirname(remove_safely(target_path)))
    symlink(normpath(source_path), target_path)
    return target_path


def find_path(file_name, folder):
    'Locate file in folder'
    for root_folder, folder_names, file_names in walk(folder):
        if file_name in file_names:
            file_path = join(root_folder, file_name)
            break
    else:
        raise IOError('cannot find {0} in {1}'.format(file_name, folder))
    return file_path


def find_paths(name_expression, folder):
    'Locate files in folder matching expression'
    return [
        join(root_folder, file_name)
        for root_folder, folder_names, file_names in walk(folder)
        for file_name in fnmatch.filter(file_names, name_expression)]


def resolve_relative_path(relative_path, folder):
    relative_path = relpath(join(folder, relative_path), folder)
    if relative_path.startswith('..'):
        raise IOError('relative_path must refer to a file inside folder')
    return join(folder, relative_path)


def compress(source_folder, target_path=None, excludes=None):
    'Compress folder; specify archive extension (.tar.gz .zip) in target_path'
    if not target_path:
        target_path = source_folder + '.tar.gz'
    if target_path.endswith('.tar.gz'):
        compress_tar_gz(source_folder, target_path, excludes)
    else:
        compress_zip(source_folder, target_path, excludes)
    return target_path


def compress_tar_gz(source_folder, target_path=None, excludes=None):
    'Compress folder as tar archive'
    if not target_path:
        target_path = source_folder + '.tar.gz'
    with tarfile.open(target_path, 'w:gz', dereference=True) as target_file:
        for path in Path(source_folder).rglob('*'):
            if path.is_dir():
                continue
            if has_name_match(path, excludes):
                continue
            target_file.add(str(path), str(path.relative_to(source_folder)))
    return target_path


def compress_zip(source_folder, target_path=None, excludes=None):
    'Compress folder as zip archive'
    if not target_path:
        target_path = source_folder + '.zip'
    with ZipFile(
        target_path, 'w', ZIP_DEFLATED, allowZip64=True,
    ) as target_file:
        for path in Path(source_folder).rglob('*'):
            if path.is_dir():
                continue
            if has_name_match(path, excludes):
                continue
            target_file.write(
                str(path), str(path.relative_to(source_folder)))
    return target_path


def uncompress(source_path, target_folder=None):
    if source_path.endswith('.tar.gz'):
        source_file = tarfile.open(source_path, 'r:gz')
        default_target_folder = re.sub(r'\.tar.gz$', '', source_path)
    else:
        source_file = ZipFile(source_path, 'r')
        default_target_folder = re.sub(r'\.zip$', '', source_path)
    target_folder = target_folder or default_target_folder
    source_file.extractall(target_folder)
    source_file.close()
    return target_folder


def are_same_path(path1, path2):
    return realpath(path1) == realpath(path2)


def has_name_match(path, expressions):
    name = basename(str(path))
    for expression in expressions or []:
        if fnmatch.fnmatch(name, expression):
            return True
    return False


@contextmanager
def cd(target_folder):
    source_folder = getcwd()
    try:
        chdir(target_folder)
        yield
    finally:
        chdir(source_folder)


@contextmanager
def make_temporary_path(suffix='', prefix='tmp', target_folder=None):
    temporary_path = mkstemp(suffix, prefix, target_folder)
    yield temporary_path
    rmtree(temporary_path)


@contextmanager
def make_temporary_folder(suffix='', prefix='tmp', target_folder=None):
    temporary_folder = mkdtemp(suffix, prefix, target_folder)
    yield temporary_folder
    rmtree(temporary_folder)


def make_enumerated_folder_for(script_path, first_index=1):
    package_name = get_file_basename(script_path)
    if 'run' == package_name:
        package_folder = get_package_folder(script_path)
        package_name = get_file_basename(package_folder)
    return make_enumerated_folder(join(sep, 'tmp', package_name), first_index)


def make_enumerated_folder(base_folder, first_index=1):
    'Make a unique enumerated folder in base_folder'

    def suggest_folder(index):
        return join(base_folder, str(index))

    target_index = first_index
    target_folder = suggest_folder(target_index)
    while True:
        try:
            makedirs(target_folder)
            break
        except OSError:
            target_index += 1
            target_folder = suggest_folder(target_index)
    return target_folder


def get_package_folder(script_path):
    return dirname(abspath(script_path))


def change_owner_and_group_recursively(target_folder, target_username):
    'Change uid and gid of folder and its contents, treating links as files'
    from os import lchown     # Undefined in Windows
    from pwd import getpwnam  # Undefined in Windows
    pw_record = getpwnam(target_username)
    target_uid = pw_record.pw_uid
    target_gid = pw_record.pw_gid
    for root_folder, folders, names in walk(target_folder):
        for folder in folders:
            lchown(join(root_folder, folder), target_uid, target_gid)
        for name in names:
            lchown(join(root_folder, name), target_uid, target_gid)
    lchown(target_folder, target_uid, target_gid)


def get_file_basename(path):
    'Return file name without extension (x/y/z/file.txt -> file)'
    return splitext(basename(path))[0]


def get_file_extension(file_name, max_length=16):
    # Extract extension
    try:
        file_extension = file_name.split('.', 1)[1]
    except IndexError:
        return ''
    # Sanitize characters
    file_extension = ''.join(x for x in file_extension if x.isalnum() or x in [
        ',', '-', '_',
    ]).rstrip()
    # Limit length
    return '.' + file_extension[-max_length:]
