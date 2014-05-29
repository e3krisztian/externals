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

    def read(self, overlay):
        return overlay.content

    def write(self, overlay, value):
        overlay.content = value

    def test_readonly_proxied(self):
        f = OverlayFixture(readonly_text=SOME_TEXT)
        self.assertEquals(SOME_TEXT, self.read(f.overlay))

    def test_writable_has_precedence_over_readonly(self):
        f = OverlayFixture(
            readonly_text=SOME_TEXT,
            writable_text=SOME_OTHER_TEXT,
        )
        self.assertEquals(SOME_OTHER_TEXT, self.read(f.overlay))

    def test_overwriting_do_not_change_readonly(self):
        f = OverlayFixture(readonly_text=SOME_TEXT)

        self.write(f.writable, SOME_OTHER_TEXT)

        self.assertEquals(SOME_TEXT, self.read(f.readonly))
        self.assertEquals(SOME_OTHER_TEXT, self.read(f.overlay))

    def test_deleted_content_is_still_unchanged_in_readonly(self):
        f = OverlayFixture(readonly_text=SOME_TEXT)

        f.overlay.delete()

        self.assertEquals(SOME_TEXT, self.read(f.readonly))

    def test_translated_readonly_proxied(self):
        f = OverlayFixture(readonly_text=SOME_TEXT, path=SOME_PATH)
        self.assertEquals(SOME_TEXT, self.read(f.overlay))

    def test_translated_writable_has_precedence_over_readonly(self):
        f = OverlayFixture(
            readonly_text=SOME_TEXT,
            writable_text=SOME_OTHER_TEXT,
            path=SOME_PATH,
        )
        self.assertEquals(SOME_OTHER_TEXT, self.read(f.overlay))

    def test_translated_overwriting_do_not_change_readonly(self):
        f = OverlayFixture(readonly_text=SOME_TEXT, path=SOME_PATH)

        self.write(f.writable / SOME_PATH, SOME_OTHER_TEXT)

        self.assertEquals(SOME_TEXT, self.read(f.readonly / SOME_PATH))
        self.assertEquals(SOME_OTHER_TEXT, self.read(f.overlay))

    def test_translated_deleted_content_is_still_unchanged_in_readonly(self):
        f = OverlayFixture(readonly_text=SOME_TEXT, path=SOME_PATH)

        f.overlay.delete()

        self.assertEquals(SOME_TEXT, self.read(f.readonly / SOME_PATH))

    def test_set_content_can_be_read_back(self):
        f = OverlayFixture(readonly_text=SOME_TEXT, path=SOME_PATH)
        self.write(f.overlay, SOME_OTHER_TEXT)
        self.assertEquals(SOME_OTHER_TEXT, self.read(f.overlay))

    def test_set_deleted_content_can_be_read_back(self):
        f = OverlayFixture(readonly_text=SOME_TEXT, path=SOME_PATH)
        f.overlay.delete()

        self.write(f.overlay, SOME_OTHER_TEXT)
        self.assertEquals(SOME_OTHER_TEXT, self.read(f.overlay))

    def test_delete_makes_content_unavailable(self):
        f = OverlayFixture(readonly_text=SOME_TEXT, path=SOME_PATH)

        f.overlay.delete()

        with self.assertRaises(NoContentError):
            self.read(f.overlay)

    def test_delete_leaves_content_below_available(self):
        f = OverlayFixture(readonly_text=SOME_TEXT, path=SOME_PATH)
        self.write(f.readonly, SOME_OTHER_TEXT)

        f.overlay.delete()

        self.assertEquals(SOME_OTHER_TEXT, self.read(f.root_overlay))

    def test_deleted_content_is_seen_as_deleted_through_another_external(self):
        f = OverlayFixture(readonly_text=SOME_TEXT, path=SOME_PATH)
        self.write(f.readonly, SOME_OTHER_TEXT)

        f.overlay.delete()

        with self.assertRaises(Exception):
            self.read(f.root_overlay / SOME_PATH)


class Test_Overlay_content_from_streams(Test_Overlay_content):

    def read(self, overlay):
        with overlay.readable_stream() as s:
            return s.read()

    def write(self, overlay, value):
        with overlay.writable_stream() as s:
            return s.write(value)


class Test_Overlay_delete(unittest.TestCase):

    def test_makes_itself_nonexistent(self):
        f = OverlayFixture(readonly_text=SOME_TEXT, path=SOME_PATH)

        f.overlay.delete()

        self.assertFalse(f.overlay.exists())


class Test_Overlay_is_file(unittest.TestCase):

    def test_readable_content(self):
        f = OverlayFixture(readonly_text=SOME_TEXT, path=SOME_PATH)

        self.assertTrue(f.overlay.is_file())

    def test_writable_content(self):
        f = OverlayFixture(writable_text=SOME_TEXT, path=SOME_PATH)

        self.assertTrue(f.overlay.is_file())


class Test_Overlay_is_dir(unittest.TestCase):

    def test_readable_content(self):
        f = OverlayFixture(readonly_text=SOME_TEXT, path=SOME_PATH)

        self.assertTrue(f.overlay.parent().is_dir())

    def test_writable_content(self):
        f = OverlayFixture(writable_text=SOME_TEXT, path=SOME_PATH)

        self.assertTrue(f.overlay.parent().is_dir())
