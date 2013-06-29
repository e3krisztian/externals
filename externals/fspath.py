from externals.external import External
from externals.external import NoParentError
import os
import shutil


class FsPath(External):

    def __init__(self, path):
        self._path = os.path.realpath(path)

    @property
    def name(self):
        parent, tail = os.path.split(self._path)
        return tail

    def parent(self):
        new_path, tail = os.path.split(self._path)
        if not tail:
            raise NoParentError
        return FsPath(new_path)

    def __div__(self, sub_path):
        '''Build new externals for contained sub_path

        x / u'name'
        x / u'name1/name2/name3'
        '''
        # FIXME: take care of (forbid?) /./ and /../ constructs
        return FsPath(
            os.path.join(
                self._path,
                sub_path.strip(os.path.sep)))

    def exists(self):
        return os.path.exists(self._path)

    def is_file(self):
        return os.path.isfile(self._path)

    def content(self):
        with self.readable_stream() as f:
            return f.read()

    def set_content(self, content):
        parent, tail = os.path.split(self._path)
        if not os.path.exists(parent):
            os.makedirs(parent)

        with self.writable_stream() as f:
            f.write(content)

    def readable_stream(self):
        return open(self._path, u'rb')

    def writable_stream(self):
        return open(self._path, u'wb')

    def is_dir(self):
        return os.path.isdir(self._path)

    def __iter__(self):
        for name in os.listdir(self._path):
            yield self / name

    def remove(self):
        shutil.rmtree(self._path)


def working_directory():
    return FsPath('.')
