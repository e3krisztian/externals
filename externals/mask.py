import itertools

from .trie import Trie


NOT_COVERED = 'NOT_COVERED'
COVERED = 'COVERED'
CHILDREN_COVERED = 'CHILDREN_COVERED'


class Mask(Trie):

    def __init__(self):
        super(Mask, self).__init__()
        self._root.content = NOT_COVERED

    def drill(self, path):
        last, remaining = self._get_last_and_missing(path)
        if last.content == NOT_COVERED:
            # already not covered
            return

        # force downgrade from COVERED
        last.content = CHILDREN_COVERED
        if remaining:
            self.extend(path, itertools.repeat(CHILDREN_COVERED))

    def covered(self, path):
        last, remaining = self._get_last_and_missing(path)
        return self._covered(last, remaining)

    def _covered(self, last, remaining):
        if remaining:
            return last.content != NOT_COVERED
        return last.content == COVERED

    def cover(self, path):
        last, remaining = self._get_last_and_missing(path)
        if self._covered(last, remaining):
            # assert self.covered(path)
            return

        # currently visible
        if remaining:
            assert last.content == NOT_COVERED
            self.extend(path, [NOT_COVERED] * (len(path) - 1) + [COVERED])
        else:
            last.content = COVERED
            last.children = None

        # assert self.covered(path)
