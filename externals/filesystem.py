from . import HierarchicalExternal
import os
import shutil


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
