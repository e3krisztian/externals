from externals.external import External, NoParentError
import io
import contextlib


PATH_SEPARATOR = '/'

# InMemoryFileSystem nodes are dictionaries,
# with known keys (all of them are optional):
# additional metadata can be supported by adding new keys

KEY_CHILDREN = 'children'  # directory behavior
KEY_CONTENT = 'content'  # file behavior


class InMemoryFileSystem(object):

    def __init__(self):
        self.root = {KEY_CHILDREN: {}}

    def __getitem__(self, path):
        node = self.root
        for name in path:
            if KEY_CHILDREN not in node:
                raise KeyError(path)
            subdirs = node[KEY_CHILDREN]
            node = subdirs[name]
        return node

    def ensure(self, path):
        node = self.root
        for name in path:
            if KEY_CHILDREN not in node:
                node[KEY_CHILDREN] = {}
            subdirs = node[KEY_CHILDREN]
            if name not in subdirs:
                subdirs[name] = {}
            node = subdirs[name]


class Memory(External):

    '''I am not an external, but pretend to be: hold data in memory.'''

    def __init__(self, fs=None, path=None):
        self._fs = fs or InMemoryFileSystem()
        self._path = tuple(part for part in path if part) if path else ()

    @property
    def _node(self):
        return self._fs[self._path]

    def _new(self, path):
        return self.__class__(self._fs, path)

    def parent(self):
        if not self._path:
            raise NoParentError
        return self._new(self._path[:-1])

    def exists(self):
        try:
            self._node
            return True
        except KeyError:
            return False

    @property
    def name(self):
        return self._path[-1] if self._path else ''

    def __div__(self, sub_path):
        '''Build new externals for contained sub_path

        x / 'name'
        x / 'name1/name2/name3'
        '''
        return self._new(self._path + tuple(sub_path.split(PATH_SEPARATOR)))

    def is_file(self):
        try:
            return KEY_CONTENT in self._node
        except KeyError:
            return False

    # .content
    def content():
        def fget(self):
            return self._node[KEY_CONTENT]

        def fset(self, value):
            # Create file with content and missing directories up to the file
            self._fs.ensure(self._path)
            self._node[KEY_CONTENT] = value
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

    def is_dir(self):
        try:
            return KEY_CHILDREN in self._node
        except KeyError:
            return False

    def __iter__(self):
        ''' Iterator over children '''
        subdir = self._node[KEY_CHILDREN]
        return (
            self / name
            for name in subdir)

    def delete(self):
        try:
            self._node.clear()
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
