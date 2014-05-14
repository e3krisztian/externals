from .external import NoParentError


class NotFoundError(LookupError):
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
