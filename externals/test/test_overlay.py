from __future__ import unicode_literals

import unittest

import externals.overlay as m
from externals import Memory, NoContentError
from externals.mask import Mask

SOME_TEXT = b'some content'
SOME_OTHER_TEXT = b'some other content'

assert SOME_TEXT != SOME_OTHER_TEXT

SOME_PATH = 'some/path'


class OverlayFixture(object):

    def __init__(self, readonly_text=None, writable_text=None, path=''):
        self.readonly = Memory()
        if readonly_text is not None:
            (self.readonly / path).content = readonly_text

        self.writable = Memory()
        if writable_text is not None:
            (self.writable / path).content = writable_text

        self.mask = Mask()

        self.root_overlay = m.Overlay(self.readonly, self.writable, self.mask)
        self.overlay = self.root_overlay / path


class Test_Overlay_content(unittest.TestCase):

    def test_readonly_proxied(self):
        f = OverlayFixture(readonly_text=SOME_TEXT)
        self.assertEquals(SOME_TEXT, f.overlay.content)

    def test_writable_has_precedence_over_readonly(self):
        f = OverlayFixture(
            readonly_text=SOME_TEXT,
            writable_text=SOME_OTHER_TEXT,
        )
        self.assertEquals(SOME_OTHER_TEXT, f.overlay.content)

    def test_overwriting_do_not_change_readonly(self):
        f = OverlayFixture(readonly_text=SOME_TEXT)

        f.writable.content = SOME_OTHER_TEXT

        self.assertEquals(SOME_TEXT, f.readonly.content)
        self.assertEquals(SOME_OTHER_TEXT, f.overlay.content)

    def test_deleted_content_is_still_unchanged_in_readonly(self):
        f = OverlayFixture(readonly_text=SOME_TEXT)

        f.overlay.delete()

        self.assertEquals(SOME_TEXT, f.readonly.content)

    def test_translated_readonly_proxied(self):
        f = OverlayFixture(readonly_text=SOME_TEXT, path=SOME_PATH)
        self.assertEquals(SOME_TEXT, f.overlay.content)

    def test_translated_writable_has_precedence_over_readonly(self):
        f = OverlayFixture(
            readonly_text=SOME_TEXT,
            writable_text=SOME_OTHER_TEXT,
            path=SOME_PATH,
        )
        self.assertEquals(SOME_OTHER_TEXT, f.overlay.content)

    def test_translated_overwriting_do_not_change_readonly(self):
        f = OverlayFixture(readonly_text=SOME_TEXT, path=SOME_PATH)

        (f.writable / SOME_PATH).content = SOME_OTHER_TEXT

        self.assertEquals(SOME_TEXT, (f.readonly / SOME_PATH).content)
        self.assertEquals(SOME_OTHER_TEXT, f.overlay.content)

    def test_translated_deleted_content_is_still_unchanged_in_readonly(self):
        f = OverlayFixture(readonly_text=SOME_TEXT, path=SOME_PATH)

        f.overlay.delete()

        self.assertEquals(SOME_TEXT, (f.readonly / SOME_PATH).content)

# TODO: test write content goes to writable
# TODO: test write potentially makes non-existent existent


class Test_Overlay_delete(unittest.TestCase):

    def test_makes_content_unavailable(self):
        f = OverlayFixture(readonly_text=SOME_TEXT, path=SOME_PATH)

        f.overlay.delete()

        with self.assertRaises(NoContentError):
            f.overlay.content

    def test_leaves_content_below_available(self):
        f = OverlayFixture(readonly_text=SOME_TEXT, path=SOME_PATH)
        f.readonly.content = SOME_OTHER_TEXT

        f.overlay.delete()

        self.assertEquals(SOME_OTHER_TEXT, f.root_overlay.content)

    def test_deleted_content_is_seen_as_deleted_through_another_external(self):
        f = OverlayFixture(readonly_text=SOME_TEXT, path=SOME_PATH)
        f.readonly.content = SOME_OTHER_TEXT

        f.overlay.delete()

        with self.assertRaises(Exception):
            (f.root_overlay / SOME_PATH).content
