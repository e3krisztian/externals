import io
import contextlib

from . import HierarchicalExternal, NoContentError
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
    def is_file(self):
        return self._fs.has_content(self.path_segments)

    def is_dir(self):
        return self._fs.is_internal(self.path_segments)

    @property
    def content(self):
        'read/write property for accessing the content of "files"'
        try:
            return self._fs[self.path_segments]
        except KeyError:
            raise NoContentError(self.path)

    @content.setter
    def content(self, value):
        self._fs[self.path_segments] = value

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
