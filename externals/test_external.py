# coding: utf8
import unittest
import os
import externals.external as m


class Locator(m.External):

    def __init__(self, path):
        self.path = path
        self._is_root = path == u'/'

    def exists(self):
        return self.path in u'/ /a /a/b /a/b/x /a/y /x /.git'.split()

    def child(self, name):
        if self._is_root:
            newpath = u'/' + name
        else:
            newpath = u'{}/{}'.format(self.path, name)
        return self.__class__(newpath)

    def parent(self):
        if self._is_root:
            raise m.NoParentError
        head, sep, tail = self.path.rpartition(u'/')
        return self.__class__(head or u'/')


class TestLocator(unittest.TestCase):

    def test_parent_of_root_raises_error(self):
        with self.assertRaises(m.NoParentError):
            Locator(u'/').parent()

    def test_parent_of_a_is_root(self):
        self.assertEqual(u'/', Locator(u'/a').parent().path)

    def test_child_of_root(self):
        self.assertEqual(u'/a', Locator(u'/').child(u'a').path)


'''
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


class TestExternal(unittest.TestCase):

    def check(self, expected, orig, name):
        self.assertEqual(expected, Locator(orig).locate(name).path)

    def test_locate_ab_b_is_ab(self):
        self.check(u'/a/b', u'/a/b', u'b')

    def test_locate_ab_x_is_abx(self):
        self.check(u'/a/b/x', u'/a/b', u'x')

    def test_locate_a_x_is_x(self):
        self.check(u'/x', u'/a', u'x')

    def test_locate_ab_y_is_ay(self):
        self.check(u'/a/y', u'/a/b', u'y')

    def test_locate_ab_y_is_ay(self):
        self.check(u'/.git', u'/a/b', u'.git')

    def test_locate_ab_z_raises_NotFoundError(self):
        with self.assertRaises(m.NotFoundError):
            Locator(u'/a/b').locate(u'z')
