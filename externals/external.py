'''
A hierarchically named resource, potentially external to the current process.

FileSystem
HTTP
REST
XML DOM - not really external, yet tree-like with content
'''

class NoParentError(LookupError):
    pass


class External(object):

    @property
    def name(self):
        ''' Last name '''
        pass

    def parent(self):
        pass

    def child(self, name):
        pass

    def __add__(self, sub_path):
        ''' Syntactic sugar for child(u'name1').child(u'name2')...

        x + u'name'
        x + u'name1/name2/name3'
        '''
        pass

    def exists(self):
        pass

    def is_file(self):
        pass

    def content(self):
        pass

    def set_content(self, content):
        pass

    def readable_stream(self):
        pass

    def writable_stream(self):
        pass

    def is_dir(self):
        pass

    def children(self):
        pass

    def __iter__(self):
        ''' Iterator over children '''
        pass

    def create(self, content):
        ''' Creates the file, creates missing directories up to the file '''
        pass

    def remove(self):
        pass

    def locate(self, name):
        r''' The longest existing path, that ends in :name: and shares all, but maybe the last name with :self:.

        Examples:

        Given this structure:

        '/' - a - b
        | \    \   \
        |  x    y   x
        |
         \.git

        External( /a/b ).locate(   'b'  ) is External( /a/b   )
        External( /a/b ).locate(   'x'  ) is External( /a/b/x )
        External( /a   ).locate(   'x'  ) is External( /x     )
        External( /a/b ).locate(   'y'  ) is External( /a/y   )
        External( /a/b ).locate( '.git' ) is External( /.git  )
        '''
        pass
