# coding: utf8
import unittest
import os
from temp_dir import in_temp_dir, within_temp_dir
import externals.filesystem as m
from externals.test import common
import contextlib


class TestFsRoot(unittest.TestCase, common.RootTests):

    def _get_root(self):
        return m.File('/')


class TestFile(unittest.TestCase):

    def _get_existing_file(self):
        return m.File(__file__)

    def test_this_file_exists(self):
        self.assertTrue(self._get_existing_file().exists())

    def test_nonexistent_child_does_not_exists(self):
        x = m.File(__file__) / 'nonexistent'
        self.assertFalse(x.exists())

    def test_this_file_is_a_file(self):
        self.assertTrue(self._get_existing_file().is_file())

    def test_this_file_is_not_a_directory(self):
        self.assertFalse(self._get_existing_file().is_dir())

    def test_name_is_last_segment_of_path(self):
        x = m.File('/a/last')
        self.assertEqual('last', x.name)

    @within_temp_dir
    def test_content_returns_file_content(self):
        filename = 'test-file1'
        with open(filename, 'wb') as f:
            f.write(b'something\nand more')

        x = m.File(filename)

        self.assertEqual(b'something\nand more', x.content)

    @within_temp_dir
    def test_set_content_stores_data(self):
        filename = 'test-file2'

        x_store = m.File(filename)
        x_store.content = b'something2\nand more'

        x_read = m.File(filename)
        self.assertEqual(b'something2\nand more', x_read.content)

    @within_temp_dir
    def test_readable_stream_returns_an_open_file(self):
        filename = 'test-file3'

        x_store = m.File(filename)
        x_store.content = b'something3'

        x_read = m.File(filename)
        with x_read.readable_stream() as stream:
            self.assertEqual(b's', stream.read(1))
            self.assertEqual(b'o', stream.read(1))
            self.assertEqual(b'mething3', stream.read())

    @within_temp_dir
    def test_writable_stream_returns_an_open_file(self):
        x_tempdir = m.working_directory()

        x_store = x_tempdir / 'test-file'
        with x_store.writable_stream() as stream:
            stream.write(b's')
            stream.write(b'o')
            stream.write(b'mething4')

        x_read = x_tempdir / 'test-file'
        self.assertEqual(b'something4', x_read.content)

    @within_temp_dir
    def test_writable_stream_creates_missing_directories(self):
        x_store = m.working_directory() / 'missing directory' / 'test-file'

        # create empty file
        with x_store.writable_stream():
            pass

        x_read = m.working_directory() / 'missing directory' / 'test-file'
        self.assertEqual(b'', x_read.content)

    @within_temp_dir
    def test_children_returns_list_of_externals_for_children(self):
        x_tempdir = m.working_directory()
        (x_tempdir / 'a').content = b'a content'
        (x_tempdir / 'b').content = b'b content'
        os.mkdir('c')

        x_test = m.working_directory()

        def name(x):
            return x.name
        children = sorted(x_test.children(), key=name)

        self.assertEqual(3, len(children))
        self.assertEqual(
            ['a', 'b', 'c'],
            [name(child) for child in children])

    @within_temp_dir
    def test_external_is_an_iterable_returning_children(self):
        x_tempdir = m.working_directory()
        (x_tempdir / 'a').content = b'a content'
        (x_tempdir / 'b').content = b'b content'
        os.mkdir('c')

        x_test = m.working_directory()
        children_list = []
        # iterate over the external
        for child in x_test:
            children_list.append(child)

        def name(x):
            return x.name
        children = sorted(x_test.children(), key=name)

        self.assertEqual(3, len(children))
        self.assertEqual(
            ['a', 'b', 'c'],
            [name(child) for child in children])

    @within_temp_dir
    def test_set_content_creates_missing_directories_and_a_file(self):
        x_tempdir = m.working_directory()
        x_a = x_tempdir / 'a'
        x_ab = x_a / 'b'
        x_file = x_ab / 'c'

        x_file.content = b'content'

        with open('a/b/c', 'rb') as f:
            self.assertEqual(b'content', f.read())

    @within_temp_dir
    def test_directory_with_subdir_is_deleted(self):
        x_tempdir = m.working_directory()
        x_a = x_tempdir / 'a'
        x_ab = x_a / 'b'
        x_file = x_ab / 'c'

        x_file.content = b'content'

        x_a.delete()

        self.assertFalse(x_ab.exists())

    @within_temp_dir
    def test_adding_a_string_to_an_external_means_asking_for_a_child(self):
        x_tempdir = m.working_directory()
        (x_tempdir / 'a').content = b'child'

        self.assertEqual(b'child', (x_tempdir / 'a').content)

    @within_temp_dir
    def test_add_a_path(self):
        x_tempdir = m.working_directory()
        # file dir-a/dir-b/file
        (x_tempdir / 'dir-a' / 'dir-b' / 'file').content = b'child'

        self.assertEqual(
            b'child',
            (x_tempdir / 'dir-a/dir-b/file').content)

    @within_temp_dir
    def test_add_a_path_wrapped_in_slashes(self):
        x_tempdir = m.working_directory()
        # file dir-a/dir-b/file
        (x_tempdir / 'dir-a' / 'dir-b' / 'file').content = b'child'

        self.assertEqual(
            b'child',
            (x_tempdir / '/dir-a/dir-b/file/').content)


class Test_working_directory(unittest.TestCase):

    def test_working_directory_is_an_fspath(self):
        self.assertIsInstance(m.working_directory(), m.File)

    def test_working_directory_is_absolute(self):
        with in_temp_dir():
            x1 = m.working_directory()
            with in_temp_dir():
                x2 = m.working_directory()
                self.assertNotEqual(x1.path, x2.path)


class Test_File_copy_to(
        unittest.TestCase,
        common.BigExternal_copy_to_Tests):

    @contextlib.contextmanager
    def _get_external(self):
        with in_temp_dir():
            x = m.working_directory() / 'temporary file'
            x.content = b'something smallish'
            yield x
