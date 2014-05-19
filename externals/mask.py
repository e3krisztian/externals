import itertools

from .trie import Trie


TRANSPARENT = 'TRANSPARENT'
OPAQUE = 'OPAQUE'
TRANSPARENT_BORDER = 'TRANSPARENT_BORDER'

# path ending in a transparent border:
# the item is transparent, but its potential children,
# who are not mentioned explicitly in the mask
# as being a transparent border themselves are opaque


class Mask(Trie):

    def __init__(self):
        super(Mask, self).__init__()
        self._root.content = TRANSPARENT

    def drill(self, path):
        last, remaining = self._get_last_and_missing(path)
        if last.content == TRANSPARENT:
            # already not covered
            return

        # make just the path transparent
        last.content = TRANSPARENT_BORDER
        if remaining:
            self.extend(path, itertools.repeat(TRANSPARENT_BORDER))

    def covered(self, path):
        last, remaining = self._get_last_and_missing(path)
        return self._covered(last, remaining)

    def _covered(self, last, remaining):
        if remaining:
            return last.content != TRANSPARENT
        return last.content == OPAQUE

    def cover(self, path):
        last, remaining = self._get_last_and_missing(path)
        if self._covered(last, remaining):
            # assert self.covered(path)
            return

        # currently visible
        if remaining:
            assert last.content == TRANSPARENT
            self.extend(path, [TRANSPARENT] * (len(path) - 1) + [OPAQUE])
        else:
            last.content = OPAQUE
            last.children = None

        # assert self.covered(path)
