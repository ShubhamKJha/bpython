# -*- coding: utf-8 -*-

try:
    import unittest2 as unittest
except ImportError:
    import unittest

from bpython import inspection
from bpython.test.fodder import encoding_ascii
from bpython.test.fodder import encoding_latin1
from bpython.test.fodder import encoding_utf8

foo_ascii_only = u'''def foo():
    """Test"""
    pass
'''

foo_non_ascii = u'''def foo():
    """Test äöü"""
    pass
'''


class TestInspection(unittest.TestCase):
    def test_is_callable(self):
        class OldCallable:
            def __call__(self):
                pass

        class Callable(object):
            def __call__(self):
                pass

        class OldNoncallable:
            pass

        class Noncallable(object):
            pass

        def spam():
            pass

        self.assertTrue(inspection.is_callable(spam))
        self.assertTrue(inspection.is_callable(Callable))
        self.assertTrue(inspection.is_callable(Callable()))
        self.assertTrue(inspection.is_callable(OldCallable))
        self.assertTrue(inspection.is_callable(OldCallable()))
        self.assertFalse(inspection.is_callable(Noncallable()))
        self.assertFalse(inspection.is_callable(OldNoncallable()))
        self.assertFalse(inspection.is_callable(None))

    def test_parsekeywordpairs(self):
        # See issue #109
        def fails(spam=['-a', '-b']):
            pass

        default_arg_repr = "['-a', '-b']"
        self.assertEqual(str(['-a', '-b']), default_arg_repr,
                         'This test is broken (repr does not match), fix me.')

        argspec = inspection.getargspec('fails', fails)
        defaults = argspec[1][3]
        self.assertEqual(str(defaults[0]), default_arg_repr)

    def test_pasekeywordpairs_string(self):
        def spam(eggs="foo, bar"):
            pass

        defaults = inspection.getargspec("spam", spam)[1][3]
        self.assertEqual(repr(defaults[0]), "'foo, bar'")

    def test_parsekeywordpairs_multiple_keywords(self):
        def spam(eggs=23, foobar="yay"):
            pass

        defaults = inspection.getargspec("spam", spam)[1][3]
        self.assertEqual(repr(defaults[0]), "23")
        self.assertEqual(repr(defaults[1]), "'yay'")

    def test_get_encoding_ascii(self):
        self.assertEqual(inspection.get_encoding(encoding_ascii), 'ascii')
        self.assertEqual(inspection.get_encoding(encoding_ascii.foo), 'ascii')

    def test_get_encoding_latin1(self):
        self.assertEqual(inspection.get_encoding(encoding_latin1), 'latin1')
        self.assertEqual(inspection.get_encoding(encoding_latin1.foo),
                         'latin1')

    def test_get_encoding_utf8(self):
        self.assertEqual(inspection.get_encoding(encoding_utf8), 'utf-8')
        self.assertEqual(inspection.get_encoding(encoding_utf8.foo), 'utf-8')

    def test_get_source_ascii(self):
        self.assertEqual(inspection.get_source_unicode(encoding_ascii.foo),
                         foo_ascii_only)

    def test_get_source_utf8(self):
        self.assertEqual(inspection.get_source_unicode(encoding_utf8.foo),
                         foo_non_ascii)

    def test_get_source_latin1(self):
        self.assertEqual(inspection.get_source_unicode(encoding_latin1.foo),
                         foo_non_ascii)

if __name__ == '__main__':
    unittest.main()
