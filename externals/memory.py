import io
import contextlib

from . import HierarchicalExternal
from .trie import Trie


class Memory(HierarchicalExternal):

    '''I am not an external, but pretend to be: hold data in memory.'''

    def __init__(self, fs=None, path=None, path_segments=()):
        self._fs = fs or Trie()
        super(Memory, self).__init__(path, path_segments)

    # Path implementation
    def new(self, path_segments):
        return self.__class__(self._fs, path_segments=path_segments)

    def __iter__(self):
        ''' Iterator over children '''
        children = self._fs.children(self.path_segments)
        return ((self / name) for name in children)

    # External implementation
    def exists(self):
        try:
            self._fs[self.path_segments]
            return True
        except KeyError:
            return False

    def is_file(self):
        try:
            return self._fs[self.path_segments] is not None
        except KeyError:
            return False

    def is_dir(self):
        try:
            return self._fs.is_internal(self.path_segments)
        except KeyError:
            return False

    # .content
    def content():
        def fget(self):
            return self._fs[self.path_segments]

        def fset(self, value):
            self._fs[self.path_segments] = value
        return locals()
    content = property(
        doc='read/write property for accessing the content of "files"',
        **content())

    def readable_stream(self):
        stream = io.BytesIO()
        stream.write(self.content)
        stream.seek(0)
        return contextlib.closing(stream)

    def writable_stream(self):
        return contextlib.closing(WritableStream(self))

    def delete(self):
        try:
            self._fs.delete(self.path_segments)
        except KeyError:
            pass


class WritableStream(io.BytesIO):

    def __init__(self, external):
        io.BytesIO.__init__(self)
        self.__external = external

    def close(self):
        content = self.getvalue()
        io.BytesIO.close(self)
        self.__external.content = content
