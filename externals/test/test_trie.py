import unittest

import externals.trie as m


def trie_abcd():
    '''
    --+- a -+- b =ab
      |     |
      |     +- c =ac
      |
      +- d =d
    '''
    t = m.Trie()
    t[('a', 'b')] = 'ab'
    t[('a', 'c')] = 'ac'
    t['d'] = 'd'
    return t


class Test_Trie(unittest.TestCase):

    def test_root(self):
        t = m.Trie()
        t[()] = 'content'
        self.assertEquals('content', t[()])

    def test_contents(self):
        self.assertIsNone(trie_abcd()['a'])
        self.assertEquals('ab', trie_abcd()['a', 'b'])
        self.assertEquals('ac', trie_abcd()['a', 'c'])
        self.assertEquals('d', trie_abcd()['d'])

    def test_indexing_with_nonexisting_path_raises_KeyError(self):
        with self.assertRaises(KeyError):
            trie_abcd()[('d', 'x')]
        with self.assertRaises(KeyError):
            trie_abcd()[['x']]

    def test_setting_internal_content_leaves_others_as_is(self):
        t = trie_abcd()
        t['a'] = 'a'
        self.assertEquals('ab', t[('a', 'b')])

    def test_is_internal(self):
        self.assertTrue(trie_abcd().is_internal(['a']))
        self.assertFalse(trie_abcd().is_internal(['a', 'b']))
        self.assertFalse(trie_abcd().is_internal(['d']))

    def test_last_existing(self):
        self.assertEquals('ab', trie_abcd().last(['a', 'b']))

    def test_last_nonexisting(self):
        self.assertEquals('d', trie_abcd().last(['d', 'b', 'c']))

    def test_extend_path_keep(self):
        t = trie_abcd()
        t.extend(('d', 'x'), ('?', 'extended'))
        self.assertEquals('d', t[['d']])
        self.assertEquals('extended', t[['d', 'x']])

    def test_extend_with_no_contents(self):
        t = trie_abcd()
        t.extend(('d', 'x'))
        self.assertEquals('d', t[['d']])
        self.assertIsNone(t[['d', 'x']])

    def test_extend_with_shorter_values_raises(self):
        t = m.Trie()
        with self.assertRaises(ValueError):
            t.extend(('a', 'b'), ['a only'])

    def test_children(self):
        self.assertEquals({'a', 'd'}, set(trie_abcd().children(())))
        self.assertEquals({'b', 'c'}, set(trie_abcd().children(['a'])))
        self.assertEquals(set(), set(trie_abcd().children(['d'])))

    def test_delete(self):
        t = trie_abcd()
        t.delete(['d'])
        self.assertEquals({'a'}, set(t.children(())))
