from os.path import basename, dirname
from pytest import fixture, raises

from invisibleroads_macros.database import (
    DummyBase, FolderMixin, UserFolderMixin)


class X(FolderMixin, DummyBase):

    __tablename__ = 'folder'


class Y(UserFolderMixin, DummyBase):

    __tablename__ = 'user_folder'


class TestFolderMixin(object):

    random_length = 10
    instance_id = 100

    def test_spawn_enumerated_folder(self, data_folder):
        folder = X.spawn_folder(data_folder)
        assert basename(folder) == '1'

    def test_spawn_random_folder(self, data_folder):
        folder = X.spawn_folder(data_folder, self.random_length)
        assert len(basename(folder)) == self.random_length

    def test_get_parent_folder(self, data_folder):
        parent_folder = X.get_parent_folder(data_folder)
        assert basename(parent_folder) == X.__tablename__

    def test_get_folder(self, data_folder):
        with raises(IOError):
            X(id='../1').get_folder(data_folder)
        folder = X(id=self.instance_id).get_folder(data_folder)
        assert basename(folder) == str(self.instance_id)


class TestUserFolderMixin(object):

    random_length = 10
    instance_id = 100
    user_id = 1000

    def test_spawn_enumerated_folder(self, data_folder):
        with raises(IOError):
            Y.spawn_folder(data_folder, owner_id='../1')
        folder = Y.spawn_folder(data_folder, owner_id=self.user_id)
        assert basename(folder) == '1'
        assert basename(dirname(folder)) == str(self.user_id)
        folder = Y.spawn_folder(data_folder)
        assert basename(folder) == '1'
        assert basename(dirname(folder)) == '0'

    def test_spawn_random_folder(self, data_folder):
        with raises(IOError):
            Y.spawn_folder(data_folder, self.random_length, owner_id='../1')
        folder = Y.spawn_folder(data_folder, self.random_length, self.user_id)
        assert len(basename(folder)) == self.random_length
        assert basename(dirname(folder)) == str(self.user_id)
        folder = Y.spawn_folder(data_folder, self.random_length)
        assert len(basename(folder)) == self.random_length
        assert basename(dirname(folder)) == '0'

    def test_get_user_folder(self, data_folder):
        with raises(IOError):
            Y.get_user_folder(data_folder, owner_id='../1')
        user_folder = Y.get_user_folder(data_folder, self.user_id)
        assert basename(user_folder) == str(self.user_id)

    def test_get_folder(self, data_folder):
        with raises(IOError):
            Y(id=self.instance_id, owner_id='../1').get_folder(data_folder)
        folder = Y(id=self.instance_id, owner_id=self.user_id).get_folder(
            data_folder)
        assert basename(folder) == str(self.instance_id)


@fixture
def data_folder(tmpdir):
    return str(tmpdir)
