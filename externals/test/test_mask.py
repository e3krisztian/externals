import unittest

import externals.mask as m


# paths:
ROOT = ()
A_ = ('a',)
A_B = ('a', 'b')
A_B_C = ('a', 'b', 'c')
A_C = ('a', 'c')
B_C = ('b', 'c')
B_ = ('b',)
B_C_D = ('b', 'c', 'd')


class Test_Mask(unittest.TestCase):

    def test_root_is_not_covered_initially(self):
        mask = m.Mask()
        self.assertFalse(mask.covered(ROOT))

    def test_cover_root(self):
        mask = m.Mask()
        mask.cover(ROOT)
        self.assertTrue(mask.covered(ROOT))

    def test_drill_uncovers_path(self):
        mask = m.Mask()
        mask.cover(ROOT)
        mask.drill(A_B)
        self.assertFalse(mask.covered(A_B))
        self.assertFalse(mask.covered(A_))
        self.assertFalse(mask.covered(ROOT))

    def test_drill_leaves_siblings_covered(self):
        mask = m.Mask()
        mask.cover(ROOT)
        mask.drill(A_B)
        self.assertTrue(mask.covered(A_C))

    def test_drill_leaves_children_covered(self):
        mask = m.Mask()
        mask.cover(ROOT)
        mask.drill(A_B)
        self.assertTrue(mask.covered(A_B_C))

    def test_cover_covers_children(self):
        mask = m.Mask()
        mask.cover(ROOT)
        mask.drill(A_B)
        mask.cover(A_)
        self.assertTrue(mask.covered(A_B))

    def test_cover_does_not_cover_outside_of_branch(self):
        mask = m.Mask()
        mask.cover(A_)
        mask.drill(A_B)
        mask.cover(A_B)
        self.assertFalse(mask.covered(A_))
        self.assertFalse(mask.covered(B_))

    def test_cover_already_covered(self):
        mask = m.Mask()
        mask.cover(A_)
        mask.cover(A_B)
        self.assertTrue(mask.covered(A_))
        self.assertTrue(mask.covered(A_C))

    def test_drill_into_not_covered(self):
        mask = m.Mask()
        mask.cover(A_B)
        mask.drill(B_C)
        self.assertFalse(mask.covered(B_))
        self.assertFalse(mask.covered(B_C_D))
