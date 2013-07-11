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


class NotFoundError(LookupError):
    pass


class Hierarchy(object):

    __metaclass__ = ABCMeta

    @abstractmethod
    def parent(self):
        pass

    @abstractmethod
    def __div__(self, sub_path):
        '''Build new externals for contained sub_path

        x / 'name'
        x / 'name1/name2/name3'
        '''
        pass

    def __truediv__(self, sub_path):
        '''Build new externals for contained sub_path

        x / 'name'
        x / 'name1/name2/name3'
        '''
        return self.__div__(sub_path)

    @abstractmethod
    def exists(self):
        pass


class External(Hierarchy):

    __metaclass__ = ABCMeta

    @abstractproperty
    def name(self):
        '''Last name '''
        pass

    @abstractmethod
    def is_file(self):
        pass

    @abstractproperty
    def content(self):
        pass

    @abstractmethod
    def readable_stream(self):
        pass

    @abstractmethod
    def writable_stream(self):
        pass

    @abstractmethod
    def is_dir(self):
        pass

    def children(self):
        return list(self)

    @abstractmethod
    def __iter__(self):
        ''' Iterator over children '''
        pass

    @abstractmethod
    def remove(self):
        pass


def locate(external, name):
    ''' The longest existing path, that ends in :name: and shares all, but
    maybe the last name with :self:.

    Examples:

    Given this structure

            b -- x
           /
          a -- y
         /
    '/' +-- x
         \
          .git

    locate(External( /a/b ),   'b'  ) is External( /a/b   )
    locate(External( /a/b ),   'x'  ) is External( /a/b/x )
    locate(External( /a   ),   'x'  ) is External( /x     )
    locate(External( /a/b ),   'y'  ) is External( /a/y   )
    locate(External( /a/b ), '.git' ) is External( /.git  )
    '''
    try:
        parent = external
        while True:
            candidate = parent / name
            if candidate.exists():
                return candidate
            parent = parent.parent()
    except NoParentError:
        raise NotFoundError
