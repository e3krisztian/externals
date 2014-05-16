import unittest

import externals.mask as m


class Test_DeleteMask(unittest.TestCase):

    def test_root_is_not_covered_initially(self):
        mask = m.Mask()
        self.assertFalse(mask.covered(()))

    def test_cover_root(self):
        mask = m.Mask()
        mask.cover(())
        self.assertTrue(mask.covered(()))

    def test_drill_uncovers_path(self):
        mask = m.Mask()
        mask.cover(())
        mask.drill(('a', 'b'))
        self.assertFalse(mask.covered(('a', 'b')))
        self.assertFalse(mask.covered(('a',)))
        self.assertFalse(mask.covered(()))

    def test_drill_leaves_siblings_covered(self):
        mask = m.Mask()
        mask.cover(())
        mask.drill(('a', 'b'))
        self.assertTrue(mask.covered(('a', 'c')))

    def test_drill_leaves_children_covered(self):
        mask = m.Mask()
        mask.cover(())
        mask.drill(('a', 'b'))
        self.assertTrue(mask.covered(('a', 'b', 'c')))

    def test_cover_covers_children(self):
        mask = m.Mask()
        mask.cover(())
        mask.drill(('a', 'b'))
        mask.cover(['a'])
        self.assertTrue(mask.covered(('a', 'b')))

    def test_cover_does_not_cover_outside_of_branch(self):
        mask = m.Mask()
        mask.cover(('a',))
        mask.drill(('a', 'b'))
        mask.cover(['a', 'b'])
        self.assertFalse(mask.covered(('a',)))
        self.assertFalse(mask.covered(('b',)))

    def test_cover_already_covered(self):
        mask = m.Mask()
        mask.cover(('a',))
        mask.cover(['a', 'b'])
        self.assertTrue(mask.covered(('a',)))
        self.assertTrue(mask.covered(('a', 'c',)))

    def test_drill_into_not_covered(self):
        mask = m.Mask()
        mask.cover(('a', 'b'))
        mask.drill(('b', 'c'))
        self.assertFalse(mask.covered(['b']))
        self.assertFalse(mask.covered(['b', 'c', 'd']))
