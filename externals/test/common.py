# -*- coding: utf-8 -*-
'''
Mixin classes for testing common `External` behavior.
'''

from abc import ABCMeta, abstractmethod
import mock
from externals import external
from externals.fake import Fake


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


class External_copy_to_Tests(object):

    __metaclass__ = ABCMeta

    @abstractmethod
    def _get_external(self):  # pragma: no cover
        '''\
        I should return a `context manager`, whose value is the temporary
          external
        I will clean up the temporary external when leaving the context
          it is used in.
        '''
        pass

    def test_to_fake(self):
        mem = Fake()
        with self._get_external() as external:
            content = external.content
            external.copy_to(mem)

        self.assertEqual(content, mem.content)

    def test_from_fake(self):
        mem = Fake()
        mem.content = 'small something'

        with self._get_external() as external:
            mem.copy_to(external)

            self.assertEqual('small something', external.content)


class BigExternal_copy_to_Tests(External_copy_to_Tests):

    def test_incomplete_reads_are_concatenated(self):
        mem = Fake()
        with self._get_external() as external:
            def create_fragmenting_reader():
                class Reader(object):

                    def __init__(self, fragments):
                        self._read_count = 0
                        self._fragments = fragments

                    def read(self, *args, **kwargs):
                        if self._read_count >= len(self._fragments):
                            raise EOFError
                        value = self._fragments[self._read_count]
                        self._read_count += 1
                        return value

                    def __enter__(self, *args, **kwargs):
                        return self

                    def __exit__(self, *args, **kwargs):
                        pass

                return Reader(['a', 'b', 'c'])

            with mock.patch.object(
                    external, 'readable_stream', create_fragmenting_reader):
                external.copy_to(mem)

        self.assertEqual('abc', mem.content)
