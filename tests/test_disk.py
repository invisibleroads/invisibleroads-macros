from invisibleroads_macros.disk import (
    TemporaryStorage, compress, get_absolute_path, get_file_stem,
    get_file_extension, get_relative_path, make_folder, uncompress,
    TEMPORARY_FOLDER)
from invisibleroads_macros.exceptions import BadArchive, BadPath
from os import symlink
from os.path import dirname, isdir, islink, join, relpath
from pytest import fixture, raises

from conftest import FOLDER


class CompressionMixin(object):

    def test_include_external_link(self, sandbox, target_folder):
        source_folder = sandbox.source_folder
        target_path = source_folder + self.extension
        with raises(IOError):
            compress(source_folder, target_path)
            target_folder = uncompress(target_path, target_folder)
            assert_archive_contents(target_folder, sandbox)
        target_path = compress(source_folder, target_path, [
            sandbox.external_folder])
        target_folder = uncompress(target_path, target_folder)
        assert_archive_contents(target_folder, sandbox)

    def test_resolve_source_folder_link(self, sandbox, target_folder):
        source_folder = sandbox.source_folder_link_path
        target_path = source_folder + self.extension
        compress(source_folder, target_path, [
            sandbox.external_folder])
        target_folder = uncompress(target_path, target_folder)
        assert_archive_contents(target_folder, sandbox)

    def test_recognize_bad_archive(self, tmpdir):
        target_path = str(tmpdir.join('x' + self.extension))
        open(target_path, 'wt').write('123')
        with raises(BadArchive):
            uncompress(target_path)


class TestCompressTarGz(CompressionMixin):
    extension = '.tar.gz'


class TestCompressTarXz(CompressionMixin):
    extension = '.tar.xz'


class TestCompressZip(CompressionMixin):
    extension = '.zip'


class TestTemporaryStorage(object):

    def test_parent_folder(self):
        with TemporaryStorage() as storage:
            assert storage.folder.startswith(TEMPORARY_FOLDER)
        with TemporaryStorage('/tmp') as storage:
            assert storage.folder.startswith('/tmp/')


class Object(object):
    pass


def test_get_file_stem():
    assert get_file_stem('file.txt.zip') == 'file'


def test_get_file_extension():
    assert get_file_extension('file.txt.zip') == '.txt.zip'


def test_get_relative_path():
    x = 'file.txt'
    f1 = join(FOLDER, 'folder1')
    f2 = join(FOLDER, 'folder2')
    assert get_relative_path('', f1) == ''
    assert get_relative_path(None, f1) is None
    assert get_relative_path(x, f1) == x
    assert get_relative_path(join(f1, x), f1) == x
    # Do not allow paths whose links resolve outside the folder
    with raises(BadPath):
        get_relative_path(x, f2)
    # Allow paths if they are in specified external folders
    assert get_relative_path(x, f2, [f1]) == x
    assert get_relative_path(join(f1, x), f2, [f1]) == relpath(join(f1, x), f2)


@fixture
def sandbox(tmpdir):
    """
    source_folder_link -> source_folder
    source_folder
        external_file_link -> external_folder_file
        external_folder_link -> external_folder
        internal_file_link -> internal_file
        internal_file
        internal_folder_link -> internal_folder
        internal_folder
            internal_folder_file
        empty_folder
        .hidden_file
        .hidden_folder
            hidden_folder_file
    external_folder
        external_folder_file
    """
    o, temporary_folder = Object(), str(tmpdir)
    o.parent_folder = temporary_folder
    o.source_folder = make_folder(join(temporary_folder, 'source_folder'))
    o.internal_file_path = join(o.source_folder, 'internal_file')
    open(o.internal_file_path, 'wt').write('internal_file')

    o.external_folder = make_folder(join(temporary_folder, 'external_folder'))
    o.external_folder_file_path = join(
        o.external_folder, 'external_folder_file')
    open(o.external_folder_file_path, 'wt').write('external_folder_file')

    o.internal_folder = make_folder(join(o.source_folder, 'internal_folder'))
    o.internal_folder_file_path = join(
        o.internal_folder, 'internal_folder_file')
    open(o.internal_folder_file_path, 'wt').write('internal_folder_file')

    o.internal_file_link_path = join(o.source_folder, 'internal_file_link')
    symlink(o.internal_file_path, o.internal_file_link_path)

    o.external_file_link_path = join(o.source_folder, 'external_file_link')
    symlink(o.external_folder_file_path, o.external_file_link_path)

    o.external_folder_link_path = join(o.source_folder, 'external_folder_link')
    symlink(o.external_folder, o.external_folder_link_path)

    o.internal_folder_link_path = join(o.source_folder, 'internal_folder_link')
    symlink(o.internal_folder, o.internal_folder_link_path)

    o.empty_folder = make_folder(join(o.source_folder, 'empty_folder'))
    o.hidden_file_path = join(o.source_folder, '.hidden_file')
    o.hidden_folder = make_folder(join(o.source_folder, '.hidden_folder'))
    o.hidden_folder_file_path = join(o.hidden_folder, 'hidden_folder_file')
    open(o.hidden_file_path, 'wt').write('hidden_file')
    open(o.hidden_folder_file_path, 'wt').write('hidden_folder_file')

    o.source_folder_link_path = join(temporary_folder, 'source_folder_link')
    symlink(o.source_folder, o.source_folder_link_path)
    return o


@fixture
def target_folder(tmpdir):
    return str(tmpdir.join('target_folder'))


def assert_archive_contents(target_folder, sandbox):
    # Include external folder link as folder
    target_path = join(
        target_folder, 'external_folder_link', 'external_folder_file')
    assert_file_contents(target_path, sandbox.external_folder_file_path)
    assert not islink(dirname(target_path))
    # Include external file link as file
    target_path = join(target_folder, 'external_file_link')
    assert_file_contents(target_path, sandbox.external_folder_file_path)
    assert not islink(target_path)
    # Include internal file
    target_path = join(target_folder, 'internal_file')
    assert_file_contents(target_path, sandbox.internal_file_path)
    # Include empty folder
    assert isdir(join(target_folder, 'empty_folder'))
    # Include hidden file
    target_path = join(target_folder, '.hidden_file')
    assert_file_contents(target_path, sandbox.hidden_file_path)
    # Include hidden folder
    target_path = join(target_folder, '.hidden_folder', 'hidden_folder_file')
    assert_file_contents(target_path, sandbox.hidden_folder_file_path)
    # Include internal links
    # assert islink(join(target_folder, 'external_file_link_link'))
    # assert islink(join(target_folder, 'internal_file_link'))
    # assert islink(join(target_folder, 'internal_file_link_link'))
    # assert islink(join(target_folder, 'internal_folder_link'))


def assert_file_contents(target_path, source_path):
    old_text = open(source_path, 'rt').read()
    new_text = open(target_path).read()
    assert old_text == new_text
