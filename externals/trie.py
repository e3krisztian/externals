import itertools


class Node(object):

    __slots__ = ('children', 'content')

    def __init__(self, content):
        self.children = None
        self.content = content


class Trie(object):

    def __init__(self):
        self._root = Node(None)

    def __setitem__(self, path, content):
        if path:
            contents = [None] * (len(path) - 1) + [content]
            self._extend(path, contents, set_last=True)
        else:
            self._root.content = content

    def __getitem__(self, path):
        return self._get_node(path).content

    def is_internal(self, path):
        try:
            return bool(self._get_node(path).children)
        except KeyError:
            return False

    def has_content(self, path):
        try:
            return self._get_node(path).content is not None
        except KeyError:
            return False

    def last(self, path):
        '''Content of last existing node on path'''
        last, missing = self._get_last_and_missing(path)
        return last.content

    def children(self, path):
        children = self._get_node(path).children
        return children.keys() if children else ()

    def extend(self, path, contents=itertools.repeat(None)):
        '''Add missing nodes along path.

        Newly created nodes will have content takes from the respective
        element of contents sequence.

        I.e. if the `path[5]` is the first created node,
        it will have a content `contents[5]`.
        '''
        self._extend(path, contents, set_last=False)

    def delete(self, path):
        if path:
            node = self._get_node(path[:-1])
            del node.children[path[-1]]
        else:
            self._root.children = None
            self._root.content = None

    # helpers

    def _get_last_and_missing(self, path):
        node = self._root
        for i, name in enumerate(path):
            if (node.children is None) or (name not in node.children):
                return node, path[i:]

            node = node.children[name]

        return node, []

    def _get_node(self, path):
        last, missing = self._get_last_and_missing(path)
        if missing:
            raise KeyError(path)

        return last

    def _extend(self, path, contents, set_last):
        icontents = iter(contents)
        node = self._root
        for name in path:
            try:
                content = next(icontents)
            except StopIteration:
                raise ValueError
            if node.children is None:
                node.children = {}
            if name not in node.children:
                node.children[name] = Node(content)
            node = node.children[name]

        if set_last:
            node.content = content
