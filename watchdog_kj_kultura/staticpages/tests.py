from django.test import TestCase
from .templatetags.staticpages_tags import render_page_with_shortcode


class TempleTagsTestCase(TestCase):

    def test_render_page_with_shortcode_for_valid(self):
        TEST_CASE = {'[map]xxx[/map]': '<div class="map">xxx</div>',  # Basic case
                     "[map]\nxxx\n[/map]": '<div class="map">\nxxx\n</div>',  # Multiline case
                     "[map]x[/map]<b>XSS</b>": '<div class="map">x</div>&lt;b&gt;XSS&lt;/b&gt;'
                     }
        for value, expected in TEST_CASE.items():
            self.assertEqual(render_page_with_shortcode({}, value), expected)

    def test_render_page_with_shortcode_for_unchanged(self):
        TEST_CASE = ['[/map]xxx[map]',  # wrong order
                     '[map]xxx[/map',  # no end of end tag
                     '[map][/map]'  # empty tag
                     '[map]"[/map]'  # with quote - XSS protection
                     ]
        for item in TEST_CASE:
            self.assertEqual(render_page_with_shortcode({}, item), item)
