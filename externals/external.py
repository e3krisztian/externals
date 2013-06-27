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
    def child(self, name):
        pass

    @abstractmethod
    def exists(self):
        pass


class External(Hierarchy):

    __metaclass__ = ABCMeta

    @abstractproperty
    def name(self):
        ''' Last name '''
        pass

    @abstractmethod
    def __div__(self, sub_path):
        ''' Syntactic sugar for child(u'name1').child(u'name2')...

        x / u'name'
        x / u'name1/name2/name3'
        '''
        pass

    def __truediv__(self, sub_path):
        ''' Syntactic sugar for child(u'name1').child(u'name2')...

        x / u'name'
        x / u'name1/name2/name3'
        '''
        return self.__div__(sub_path)

    @abstractmethod
    def is_file(self):
        pass

    @abstractmethod
    def content(self):
        pass

    @abstractmethod
    def set_content(self, content):
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

    @abstractmethod
    def children(self):
        pass

    @abstractmethod
    def __iter__(self):
        ''' Iterator over children '''
        pass

    @abstractmethod
    def create(self, content):
        ''' Creates the file, creates missing directories up to the file '''
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

    External( /a/b ).locate(   'b'  ) is External( /a/b   )
    External( /a/b ).locate(   'x'  ) is External( /a/b/x )
    External( /a   ).locate(   'x'  ) is External( /x     )
    External( /a/b ).locate(   'y'  ) is External( /a/y   )
    External( /a/b ).locate( '.git' ) is External( /.git  )
    '''
    try:
        parent = external
        while True:
            candidate = parent.child(name)
            if candidate.exists():
                return candidate
            parent = parent.parent()
    except NoParentError:
        raise NotFoundError
