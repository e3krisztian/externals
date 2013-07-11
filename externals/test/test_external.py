# coding: utf8
import unittest
import externals.external as m


class TestHierarchy(m.Hierarchy):

    def __init__(self, path):
        self.path = path
        self._is_root = path == '/'

    def exists(self):
        return self.path in '/ /a /a/b /a/b/x /a/y /x /.git'.split()

    def __div__(self, name):
        if self._is_root:
            newpath = '/' + name
        else:
            newpath = '{}/{}'.format(self.path, name)
        return self.__class__(newpath)

    def parent(self):
        if self._is_root:
            raise m.NoParentError
        head, sep, tail = self.path.rpartition('/')
        return self.__class__(head or '/')


class Test_TestHierarchy(unittest.TestCase):

    def test_parent_of_root_raises_error(self):
        with self.assertRaises(m.NoParentError):
            TestHierarchy('/').parent()

    def test_parent_of_a_is_root(self):
        self.assertEqual('/', TestHierarchy('/a').parent().path)

    def test_child_of_root(self):
        self.assertEqual('/a', (TestHierarchy('/') / 'a').path)


'''
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


class Test_locate(unittest.TestCase):

    def check(self, expected, orig, name):
        self.assertEqual(expected, m.locate(TestHierarchy(orig), name).path)

    def test_locate_ab_b_is_ab(self):
        self.check('/a/b', '/a/b', 'b')

    def test_locate_ab_x_is_abx(self):
        self.check('/a/b/x', '/a/b', 'x')

    def test_locate_a_x_is_x(self):
        self.check('/x', '/a', 'x')

    def test_locate_ab_y_is_ay(self):
        self.check('/a/y', '/a/b', 'y')

    def test_locate_ab_y_is_git(self):
        self.check('/.git', '/a/b', '.git')

    def test_locate_ab_z_raises_NotFoundError(self):
        with self.assertRaises(m.NotFoundError):
            m.locate(TestHierarchy('/a/b'), 'z')
