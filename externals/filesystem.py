import os
import shutil

from . import HierarchicalExternal, NoContentError


class File(HierarchicalExternal):

    PATH_SEPARATOR = os.path.sep

    # Path implementation
    def parse_path(self, path):
        return super(File, self).parse_path(os.path.realpath(path))

    def __iter__(self):
        for name in os.listdir(self.path):
            yield self / name

    # External implementation
    def exists(self):
        return os.path.exists(self.path)

    def is_file(self):
        return os.path.isfile(self.path)

    def is_dir(self):
        return os.path.isdir(self.path)

    @property
    def content(self):
        'read/write property for accessing the content of "files"'
        with self.readable_stream() as f:
            return f.read()

    @content.setter
    def content(self, value):
        with self.writable_stream() as f:
            f.write(value)

    def readable_stream(self):
        try:
            return open(self.path, 'rb')
        except IOError:
            raise NoContentError(self.path)

    def writable_stream(self):
        parent, tail = os.path.split(self.path)
        if not os.path.exists(parent):
            os.makedirs(parent)

        return open(self.path, 'wb')

    def delete(self):
        shutil.rmtree(self.path)


def working_directory():
    return File('.')
