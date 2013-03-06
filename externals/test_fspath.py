# coding: utf8
import unittest
import os
from tempdir import TempDir
import externals.fspath as m


class TestFsPath(unittest.TestCase):

    def test_parent_of_root_exception(self):
        x = m.FsPath(u'/')
        with self.assertRaises(m.NoParentError):
            x.parent()

    def test_child_of_root_has_a_parent(self):
        x = m.FsPath(u'/')
        child = x.child(u'stem')
        child.parent()

    def test_this_file_exists(self):
        x = m.FsPath(__file__)
        self.assertTrue(x.exists())

    def test_nonexistent_sibling_does_not_exists(self):
        x = m.FsPath(__file__).parent().child('nonexistent')
        self.assertFalse(x.exists())

    def test_this_file_is_a_file(self):
        x = m.FsPath(__file__)
        self.assertTrue(x.is_file())

    def test_this_file_is_not_a_directory(self):
        x = m.FsPath(__file__)
        self.assertFalse(x.is_dir())

    def test_root_is_not_a_file(self):
        x = m.FsPath(u'/')
        self.assertFalse(x.is_file())

    def test_root_is_a_directory(self):
        x = m.FsPath(u'/')
        self.assertTrue(x.is_dir())

    def test_name_is_last_segment_of_path(self):
        x = m.FsPath(u'/a/last')
        self.assertEqual(u'last', x.name)

    def test_content_returns_file_content(self):
        with TempDir() as d:
            filename = os.path.join(d.name, u'test-file1')
            with open(filename, u'wb') as f:
                f.write('something\nand more')

            x = m.FsPath(filename)

            self.assertEqual('something\nand more', x.content())

    def test_set_content_stores_data(self):
        with TempDir() as d:
            filename = os.path.join(d.name, u'test-file2')

            x_store = m.FsPath(filename)
            x_store.set_content('something2\nand more')

            x_read = m.FsPath(filename)
            self.assertEqual('something2\nand more', x_read.content())

    def test_readable_stream_returns_an_open_file(self):
        with TempDir() as d:
            filename = os.path.join(d.name, u'test-file3')

            x_store = m.FsPath(filename)
            x_store.set_content('something3')

            x_read = m.FsPath(filename)
            with x_read.readable_stream() as stream:
                self.assertEqual('s', stream.read(1))
                self.assertEqual('o', stream.read(1))
                self.assertEqual('mething3', stream.read())

    def test_writable_stream_returns_an_open_file(self):
        with TempDir() as d:
            x_tempdir = m.FsPath(d.name)

            x_store = x_tempdir.child(u'test-file')
            with x_store.writable_stream() as stream:
                stream.write('s')
                stream.write('o')
                stream.write('mething4')

            x_read = x_tempdir.child(u'test-file')
            self.assertEqual('something4', x_read.content())

    def test_children_returns_list_of_externals_for_children(self):
        with TempDir() as d:
            x_tempdir = m.FsPath(d.name)
            x_tempdir.child(u'a').create('a content')
            x_tempdir.child(u'b').create('b content')
            os.mkdir(os.path.join(d.name, 'c'))

            x_test = m.FsPath(d.name)

            def name(x):
                return x.name
            children = sorted(x_test.children(), key=name)

            self.assertEqual(3, len(children))
            self.assertEqual([u'a', u'b', u'c'], map(name, children))

    def test_external_is_an_iterable_of_its_children(self):
        with TempDir() as d:
            x_tempdir = m.FsPath(d.name)
            x_tempdir.child(u'a').create('a content')
            x_tempdir.child(u'b').create('b content')
            os.mkdir(os.path.join(d.name, 'c'))

            x_test = m.FsPath(d.name)
            children_list = []
            # iterate over the external
            for child in x_test:
                children_list.append(child)

            def name(x):
                return x.name
            children = sorted(x_test.children(), key=name)

            self.assertEqual(3, len(children))
            self.assertEqual([u'a', u'b', u'c'], map(name, children))

    def test_create_creates_missing_directories_and_a_file(self):
        with TempDir() as d:
            x_tempdir = m.FsPath(d.name)
            x_a = x_tempdir.child(u'a')
            x_ab = x_a.child(u'b')
            x_file = x_ab.child(u'c')

            x_file.create('content')

            with open(os.path.join(d.name, u'a/b/c')) as f:
                self.assertEqual('content', f.read())

    def test_directory_with_subdir_is_removed(self):
        with TempDir() as d:
            x_tempdir = m.FsPath(d.name)
            x_a = x_tempdir.child(u'a')
            x_ab = x_a.child(u'b')
            x_file = x_ab.child(u'c')

            x_file.create('content')

            x_a.remove()

            self.assertFalse(x_ab.exists())

    def test_adding_a_string_to_an_external_means_asking_for_a_child(self):
        with TempDir() as d:
            x_tempdir = m.FsPath(d.name)
            x_tempdir.child(u'a').create('child')

            self.assertEqual('child', (x_tempdir / u'a').content())

    def test_add_a_path(self):
        with TempDir() as d:
            x_tempdir = m.FsPath(d.name)
            # file dir-a/dir-b/dir-c
            (x_tempdir.child(u'dir-a')
                .child(u'dir-b')
                .child('dir-c')
                .create('child'))

            self.assertEqual(
                'child', (x_tempdir / u'dir-a/dir-b/dir-c').content())

    def test_add_a_path_wrapped_in_slashes(self):
        with TempDir() as d:
            x_tempdir = m.FsPath(d.name)
            # file dir-a/dir-b/dir-c
            x_tempdir.child(
                u'dir-a').child(u'dir-b').child('dir-c').create('child')

            self.assertEqual(
                'child', (x_tempdir / u'/dir-a/dir-b/dir-c/').content())
