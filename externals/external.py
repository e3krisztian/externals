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


class Hierarchy(object):

    __metaclass__ = ABCMeta

    @abstractproperty
    def name(self):  # pragma: no cover
        '''Last name '''
        pass

    @abstractmethod
    def parent(self):  # pragma: no cover
        pass

    @abstractmethod
    def __div__(self, sub_path):  # pragma: no cover
        '''Build new externals for contained sub_path

        x / 'name'
        x / 'name1/name2/name3'
        '''
        pass

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

    @abstractproperty
    def content(self):  # pragma: no cover
        pass

    @abstractmethod
    def exists(self):  # pragma: no cover
        pass

    @abstractmethod
    def readable_stream(self):  # pragma: no cover
        pass

    @abstractmethod
    def writable_stream(self):  # pragma: no cover
        pass

    @abstractmethod
    def is_file(self):  # pragma: no cover
        pass

    @abstractmethod
    def is_dir(self):  # pragma: no cover
        pass

    @abstractmethod
    def delete(self):  # pragma: no cover
        pass

    def copy_to(self, other):
        other.content = self.content


class HierarchicalExternal(Hierarchy, External):

    __metaclass__ = ABCMeta
