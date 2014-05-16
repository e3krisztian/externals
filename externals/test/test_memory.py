# coding: utf8
import unittest
import externals.memory as m
from externals.test import common
import contextlib


class TestMemoryRoot(unittest.TestCase, common.RootTests):

    def _get_root(self):
        return m.Memory()


class Test_Memory(unittest.TestCase):

    def test_name(self):
        self.assertEqual('a name', (m.Memory() / 'a name').name)

    def test_nonexistent_child_does_not_exists(self):
        x = m.Memory() / 'nonexistent'
        self.assertFalse(x.exists())

    def test_existing_child_exists(self):
        x = m.Memory() / 'b'
        x.content = 'b content'
        self.assertTrue(x.exists())

    def test_content(self):
        x = m.Memory() / 'b'
        x.content = 'b content'
        self.assertEqual('b content', x.content)

    def test_nodes_on_the_path_to_existing_content_exist(self):
        a = m.Memory() / 'a'
        b = a / 'b'
        b.content = 'a/b content'
        self.assertTrue(a.exists())

    def test_node_with_content_is_file(self):
        x = m.Memory() / 'b'
        x.content = 'b content'
        self.assertTrue(x.is_file())

    def test_nonexisting_node_is_not_file(self):
        x = m.Memory() / 'b'
        self.assertFalse(x.is_file())

    def test_parent_of_file_is_dir(self):
        x = m.Memory() / 'a' / 'b'
        x.content = 'a/b content'
        self.assertTrue(x.parent().is_dir())

    def test_readable_stream(self):
        x = m.Memory()
        x.content = b'I am root'
        with x.readable_stream() as f:
            self.assertEqual(b'I am root', f.read())

    def test_writable_stream(self):
        x = m.Memory() / 'file123'
        with x.writable_stream() as f:
            f.write(b'FILE')
            f.write(b'1')
            f.write(b'23')
        self.assertEqual(b'FILE123', x.content)

    def test_children(self):
        x = m.Memory()
        (x / 'a' / 'b').content = 'content of a/b'
        (x / 'x').content = 'content of x'

        def name(x):
            return x.name
        a, x = sorted(x.children(), key=name)

        self.assertEqual('a', a.name)
        self.assertEqual('content of x', x.content)

    def test_delete_root_removes_all_contents(self):
        root = m.Memory()
        root.content = 'root'
        ab = root / 'a' / 'b'
        ab.content = 'content of a/b'

        root.delete()

        self.assertFalse(root.is_dir())
        self.assertFalse(root.is_file())
        self.assertFalse(ab.exists())

    def test_delete_root_makes_root_a_non_directory(self):
        root = m.Memory()
        root.delete()

        self.assertFalse(root.is_dir())

    def test_delete_a_non_root(self):
        root = m.Memory()
        root.content = 'root'
        x = root / '1'
        ab = x / 'a' / 'b'
        ab.content = 'content of a/b'

        x.delete()

        self.assertFalse(ab.exists())
        self.assertTrue('root', root.content)
        with self.assertRaises(KeyError):
            ab.content

    def test_nonexistent_path_is_not_a_directory(self):
        self.assertFalse((m.Memory() / 'a').is_dir())

    def test_delete_nonexistent_path(self):
        root = m.Memory()
        (root / 'x').content = 'expect to remain'
        (root / 'a').delete()

        self.assertEqual('expect to remain', (root / 'x').content)

    def test_slashes_as_first_characters_are_ignored(self):
        root = m.Memory()
        content = 'a /a and //a'
        (root / 'a').content = content

        self.assertEqual(content, (root / '/a').content)
        self.assertEqual(content, (root / '//a').content)

    def test_extra_slashes_ignored(self):
        root = m.Memory()
        content = 'a/b a//b/'
        (root / 'a/b').content = content

        self.assertEqual(content, (root / 'a//b/').content)


class Test_copy_to(unittest.TestCase, common.External_copy_to_Tests):

    @contextlib.contextmanager
    def _get_external(self):
        x = m.Memory()
        x.content = 'small content'
        yield x
