from __future__ import unicode_literals

import os

from . import HierarchicalExternal, NoContentError


class Overlay(HierarchicalExternal):

    def __init__(self, readonly, writable, mask, path=None, path_segments=()):
        self.layer_readonly = readonly
        self.layer_writable = writable
        self.layer_deleted = mask
        super(Overlay, self).__init__(path, path_segments)

    def __iter__(self):
        ''' Iterator over children '''
        # TODO
        return ()

    def new(self, path_segments):
        return self.__class__(
            self.layer_readonly,
            self.layer_writable,
            self.layer_deleted,
            path_segments=path_segments
        )

    # External

    def exists(self):
        # TODO
        return True

    def is_file(self):
        # TODO
        return True

    def is_dir(self):
        # TODO
        return True

    @property
    def content(self):
        if self.layer_deleted.covered(self.path_segments):
            raise NoContentError

        writable = self.layer_writable.new(self.path_segments)
        if writable.exists():
            return writable.content

        return self.layer_readonly.new(self.path_segments).content

    @content.setter
    def content(self, value):
        self.layer_deleted.drill(self.path_segments)

        writable = self.layer_writable.new(self.path_segments)
        writable.content = value

    def readable_stream(self):
        # TODO
        return open(os.devnull, 'rb')

    def writable_stream(self):
        # TODO
        return open(os.devnull, 'wb')

    def delete(self):
        self.layer_deleted.cover(self.path_segments)

    # TODO: copy_to - should be big-content aware, like in filesystem
