# coding: utf8
import unittest
import externals.fake as m
from externals.test import common
import contextlib


ROOT_PATH = ()


class Test_FS(unittest.TestCase):

    def test_access_root(self):
        fs = m.FS()
        self.assertEqual(fs.root, fs[ROOT_PATH])

    def test_access_non_existing(self):
        with self.assertRaises(KeyError):
            m.FS()[('nonexistent child')]

    def test_access_non_existing2(self):
        fs = m.FS()
        fs.ensure(['a'])
        with self.assertRaises(KeyError):
            fs[('nonexistent child')]

    def assertPathExists(self, fs, path):
        name = path[-1]
        parent_path = fs[path[:-1]]
        self.assertIn(name, parent_path[m.KEY_CHILDREN])

    def test_create_child_of_root(self):
        fs = m.FS()
        path = ['a']
        fs.ensure(path)
        self.assertPathExists(fs, path)

    def test_set_far_from_root(self):
        fs = m.FS()
        path = ['a', 'b', 'c']
        fs.ensure(path)
        self.assertPathExists(fs, path)

    def test_two_children(self):
        fs = m.FS()

        path1 = ['a', 'b', 'c1']
        fs.ensure(path1)
        self.assertPathExists(fs, path1)

        path2 = ['a', 'b', 'c2']
        fs.ensure(path2)
        self.assertPathExists(fs, path1)
        self.assertPathExists(fs, path2)


class TestFakeRoot(unittest.TestCase, common.RootTests):

    def _get_root(self):
        return m.Fake()


class Test_Fake(unittest.TestCase):

    def test_name(self):
        self.assertEqual('a name', (m.Fake() / 'a name').name)

    def test_nonexistent_child_does_not_exists(self):
        x = m.Fake() / 'nonexistent'
        self.assertFalse(x.exists())

    def test_existing_child_exists(self):
        x = m.Fake() / 'b'
        x.content = 'b content'
        self.assertTrue(x.exists())

    def test_content(self):
        x = m.Fake() / 'b'
        x.content = 'b content'
        self.assertEqual('b content', x.content)

    def test_nodes_on_the_path_to_existing_content_exist(self):
        a = m.Fake() / 'a'
        b = a / 'b'
        b.content = 'a/b content'
        self.assertTrue(a.exists())

    def test_node_with_content_is_file(self):
        x = m.Fake() / 'b'
        x.content = 'b content'
        self.assertTrue(x.is_file())

    def test_nonexisting_node_is_not_file(self):
        x = m.Fake() / 'b'
        self.assertFalse(x.is_file())

    def test_parent_of_file_is_dir(self):
        x = m.Fake() / 'a' / 'b'
        x.content = 'a/b content'
        self.assertTrue(x.parent().is_dir())

    def test_readable_stream(self):
        x = m.Fake()
        x.content = b'I am root'
        with x.readable_stream() as f:
            self.assertEqual(b'I am root', f.read())

    def test_writable_stream(self):
        x = m.Fake() / 'file123'
        with x.writable_stream() as f:
            f.write(b'FILE')
            f.write(b'1')
            f.write(b'23')
        self.assertEqual(b'FILE123', x.content)

    def test_children(self):
        x = m.Fake()
        (x / 'a' / 'b').content = 'content of a/b'
        (x / 'x').content = 'content of x'

        def name(x):
            return x.name
        a, x = sorted(x.children(), key=name)

        self.assertEqual('a', a.name)
        self.assertEqual('content of x', x.content)

    def test_remove_root_removes_all_contents(self):
        root = m.Fake()
        root.content = 'root'
        ab = root / 'a' / 'b'
        ab.content = 'content of a/b'

        root.remove()

        with self.assertRaises(KeyError):
            root.content
        self.assertFalse(ab.exists())

    def test_remove_root_makes_root_a_non_directory(self):
        root = m.Fake()
        root.remove()

        self.assertFalse(root.is_dir())

    def test_remove_a_non_root(self):
        root = m.Fake()
        root.content = 'root'
        x = root / '1'
        ab = x / 'a' / 'b'
        ab.content = 'content of a/b'

        x.remove()

        self.assertFalse(ab.exists())
        self.assertTrue('root', root.content)
        with self.assertRaises(KeyError):
            ab.content

    def test_nonexistent_path_is_not_a_directory(self):
        self.assertFalse((m.Fake() / 'a').is_dir())

    def test_remove_nonexistent_path(self):
        root = m.Fake()
        (root / 'x').content = 'expect to remain'
        (root / 'a').remove()

        self.assertEqual('expect to remain', (root / 'x').content)

    def test_slashes_as_first_characters_are_ignored(self):
        root = m.Fake()
        content = 'a /a and //a'
        (root / 'a').content = content

        self.assertEqual(content, (root / '/a').content)
        self.assertEqual(content, (root / '//a').content)

    def test_extra_slashes_ignored(self):
        root = m.Fake()
        content = 'a/b a//b/'
        (root / 'a/b').content = content

        self.assertEqual(content, (root / 'a//b/').content)


class Test_copy_to(unittest.TestCase, common.External_copy_to_Tests):

    @contextlib.contextmanager
    def _get_external(self):
        x = m.Fake()
        x.content = 'small content'
        yield x
