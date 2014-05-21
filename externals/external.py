'''
A hierarchically named resource, potentially external to the current process.

possible such resources are:
FileSystem
HTTP
REST
Amazon S3
XML DOM - not really external, yet tree-like with content
'''
from abc import ABCMeta, abstractmethod, abstractproperty


class NoParentError(LookupError):
    pass


class NoContentError(LookupError):
    '''External does not have content (yet)'''
    # raised for .content and .readable_stream


class Path(object):

    __metaclass__ = ABCMeta
    PATH_SEPARATOR = '/'
    ROOT = PATH_SEPARATOR

    def __init__(self, path=None, path_segments=()):
        if path:
            assert not path_segments
            path_segments = self.parse_path(path)
        self.path_segments = tuple(
            segment
            for segment in path_segments
            if segment
        )

    def new(self, path_segments):
        '''
        Create a new Path from path segments,
        potentially passing around some shared view of the world.
        '''
        return self.__class__(path_segments=path_segments)

    @property
    def name(self):
        if self.is_root:
            return self.ROOT
        return self.path_segments[-1]

    @property
    def is_root(self):
        return not self.path_segments

    @property
    def path(self):
        '''Path to me as a string'''
        return self.ROOT + self.PATH_SEPARATOR.join(self.path_segments)

    def parse_path(self, path):
        '''Return path segments
        '''
        return path.split(self.PATH_SEPARATOR)

    def parent(self):
        if self.is_root:
            raise NoParentError
        return self.new(self.path_segments[:-1])

    def __div__(self, sub_path):
        '''Build new externals for contained sub_path

        x / 'name'
        x / 'name1/name2/name3'
        '''
        # TODO: decide to allow . and .. or not - and handle them
        path_segments = self.path_segments + tuple(
            segment
            for segment in sub_path.split(self.PATH_SEPARATOR)
        )
        return self.new(path_segments)

    def __truediv__(self, sub_path):  # pragma: no cover
        '''Build new externals for contained sub_path

        x / 'name'
        x / 'name1/name2/name3'
        '''
        return self.__div__(sub_path)

    def children(self):
        return list(self)

    @abstractmethod
    def __iter__(self):  # pragma: no cover
        ''' Iterator over children '''
        pass


class External(object):

    __metaclass__ = ABCMeta

    @abstractmethod
    def exists(self):  # pragma: no cover
        pass

    @abstractmethod
    def is_file(self):  # pragma: no cover
        pass

    @abstractmethod
    def is_dir(self):  # pragma: no cover
        pass

    @abstractproperty
    def content(self):  # pragma: no cover
        pass

    @abstractmethod
    def readable_stream(self):  # pragma: no cover
        pass

    @abstractmethod
    def writable_stream(self):  # pragma: no cover
        pass

    @abstractmethod
    def delete(self):  # pragma: no cover
        pass

    def copy_to(self, other):
        other.content = self.content


class HierarchicalExternal(Path, External):

    __metaclass__ = ABCMeta
