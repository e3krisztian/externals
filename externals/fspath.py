from externals.external import External
from externals.external import NoParentError
import os
import shutil


class File(External):

    def __init__(self, path):
        self.path = os.path.realpath(path)

    @property
    def name(self):
        parent, tail = os.path.split(self.path)
        return tail

    def parent(self):
        new_path, tail = os.path.split(self.path)
        if not tail:
            raise NoParentError
        return File(new_path)

    def __div__(self, sub_path):
        '''Build new externals for contained sub_path

        x / 'name'
        x / 'name1/name2/name3'
        '''
        # FIXME: take care of (forbid?) /./ and /../ constructs
        return File(
            os.path.join(
                self.path,
                sub_path.strip(os.path.sep)))

    def exists(self):
        return os.path.exists(self.path)

    def is_file(self):
        return os.path.isfile(self.path)

    # .content
    def content():
        def fget(self):
            with self.readable_stream() as f:
                return f.read()

        def fset(self, value):
            with self.writable_stream() as f:
                f.write(value)

        return locals()
    content = property(
        doc='read/write property for accessing the content of "files"',
        **content())

    def readable_stream(self):
        return open(self.path, 'rb')

    def writable_stream(self):
        parent, tail = os.path.split(self.path)
        if not os.path.exists(parent):
            os.makedirs(parent)

        return open(self.path, 'wb')

    def is_dir(self):
        return os.path.isdir(self.path)

    def __iter__(self):
        for name in os.listdir(self.path):
            yield self / name

    def delete(self):
        shutil.rmtree(self.path)

    MAX_BLOCK_SIZE = 1 * 1024 ** 2

    def copy_to(self, other):
        max_block_size = self.MAX_BLOCK_SIZE
        with self.readable_stream() as source:
            with other.writable_stream() as destination:
                while True:
                    try:
                        block = source.read(max_block_size)
                    except EOFError:
                        break
                    if not block:
                        break
                    destination.write(block)


def working_directory():
    return File('.')
