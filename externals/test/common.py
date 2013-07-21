# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod
from externals import external


class RootTests(object):

    __metaclass__ = ABCMeta

    @abstractmethod
    def _get_root(self):  # pragma: no cover
        pass

    def test_parent_of_root_exception(self):
        with self.assertRaises(external.NoParentError):
            self._get_root().parent()

    def test_child_of_root_has_a_parent(self):
        child = self._get_root() / 'stem'
        child.parent()

    def test_root_is_not_a_file(self):
        self.assertFalse(self._get_root().is_file())

    def test_root_is_a_directory(self):
        self.assertTrue(self._get_root().is_dir())

    def test_root_exists(self):
        self.assertTrue(self._get_root().exists())
