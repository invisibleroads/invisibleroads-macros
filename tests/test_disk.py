from os import symlink
from os.path import join
from pytest import fixture, raises
from shutil import rmtree
from tempfile import mkdtemp

from invisibleroads_macros.disk import make_folder, compress, uncompress
from invisibleroads_macros.exceptions import BadArchive


@fixture(scope='module')
def sandbox(request):
    """
    source_folder_link -> source_folder
    source_folder
        internal.txt
        internal_link -> internal.txt
        external_link -> external.txt
    external.txt
    """
    temporary_folder = mkdtemp()
    o = O()
    o.source_folder = make_folder(join(temporary_folder, 'source_folder'))
    o.internal_path = join(o.source_folder, 'internal.txt')
    o.external_path = join(temporary_folder, 'external.txt')
    open(o.internal_path, 'wt').write('internal')
    open(o.external_path, 'wt').write('external')

    o.internal_link_path = join(o.source_folder, 'internal_link')
    o.external_link_path = join(o.source_folder, 'external_link')
    symlink(o.internal_path, o.internal_link_path)
    symlink(o.external_path, o.external_link_path)

    o.source_folder_link_path = join(temporary_folder, 'source_folder_link')
    symlink(o.source_folder, o.source_folder_link_path)

    yield o
    rmtree(temporary_folder)


class O(object):
    pass


class CompressionMixin(object):

    def test_include_external_link(self, sandbox, tmpdir):
        source_folder = sandbox.source_folder
        target_path = compress(source_folder, source_folder + self.extension)
        target_folder = uncompress(target_path, str(tmpdir))
        assert_contents(target_folder, sandbox)

    def test_resolve_source_folder_link(self, sandbox, tmpdir):
        source_folder = sandbox.source_folder_link_path
        target_path = compress(source_folder, source_folder + self.extension)
        target_folder = uncompress(target_path, str(tmpdir))
        assert_contents(target_folder, sandbox)

    def test_recognize_bad_archive(self, tmpdir):
        target_path = str(tmpdir.join('x' + self.extension))
        open(target_path, 'wt').write('123')
        with raises(BadArchive):
            uncompress(target_path)


class TestCompressTar(CompressionMixin):
    extension = '.tar.gz'


class TestCompressZip(CompressionMixin):
    extension = '.zip'


def assert_contents(target_folder, sandbox):
    # Include internal file
    old_text = open(sandbox.internal_path, 'rt').read()
    new_text = open(join(target_folder, 'internal.txt')).read()
    assert old_text == new_text
    # Include external link
    old_text = open(sandbox.external_path, 'rt').read()
    new_text = open(join(target_folder, 'external_link')).read()
    assert old_text == new_text
