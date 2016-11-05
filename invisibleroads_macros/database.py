from os.path import basename, join

from .descriptor import classproperty
from .disk import (
    make_enumerated_folder, make_unique_folder, resolve_relative_path)
from .security import make_random_string
from .text import lower_first_character


class DummyBase(object):

    def __init__(self, **kw):
        self.__dict__.update(kw)


class FolderMixin(object):

    @classmethod
    def spawn(Class, data_folder, random_length=None, *args, **kw):
        instance = Class()
        instance.folder = Class.spawn_folder(
            data_folder, random_length, *args, **kw)
        instance.id = basename(instance.folder)
        return instance

    @classmethod
    def spawn_folder(Class, data_folder, random_length=None):
        parent_folder = Class.get_parent_folder(data_folder)
        return make_unique_folder(
            parent_folder, make_random_string(random_length - 6)
        ) if random_length else make_enumerated_folder(parent_folder)

    @classmethod
    def get_parent_folder(Class, data_folder):
        return join(data_folder, Class._plural)

    @classproperty
    def _plural(Class):
        name = getattr(Class, '__name__', Class.__class__.__name__)
        return lower_first_character(name) + 's'

    def get_folder(self, data_folder):
        parent_folder = self.get_parent_folder(data_folder)
        return resolve_relative_path(str(self.id), parent_folder)


class UserFolderMixin(FolderMixin):

    @classmethod
    def spawn_folder(Class, data_folder, random_length=None, owner_id=None):
        user_folder = Class.get_user_folder(data_folder, owner_id)
        return make_unique_folder(
            user_folder, make_random_string(random_length - 6)
        ) if random_length else make_enumerated_folder(user_folder)

    @classmethod
    def get_user_folder(Class, data_folder, owner_id):
        parent_folder = Class.get_parent_folder(data_folder)
        return resolve_relative_path(str(owner_id or 0), parent_folder)

    def get_folder(self, data_folder):
        user_folder = self.get_user_folder(data_folder, self.owner_id)
        return resolve_relative_path(str(self.id), user_folder)
