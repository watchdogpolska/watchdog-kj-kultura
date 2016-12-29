from django.test import TestCase
from .templatetags.staticpages_tags import render_page_with_shortcode


ESCAPED_TEXT = '<div class="magnifier"><a href="x"><img src="x" class="img-responsive" />' + \
               '</a></div>&lt;b&gt;XSS&lt;/b&gt;'

MULTILINE_TEXT = '<div class="magnifier"><a href="xxx"><img src="xxx" class="img-responsive" />' + \
                 '</a></div>'

BASIC_TEXT = MULTILINE_TEXT


class TempleTagsTestCase(TestCase):

    def test_render_page_with_shortcode_for_valid(self):
        TEST_CASE = {'[map]xxx[/map]': BASIC_TEXT,           # Basic case
                     "[map]\nxxx\n[/map]": MULTILINE_TEXT,   # Multiline case
                     "[map]x[/map]<b>XSS</b>": ESCAPED_TEXT  # Tests of escaped text
                     }
        for value, expected in TEST_CASE.items():
            self.assertHTMLEqual(render_page_with_shortcode({}, value, safe=False), expected)

    def test_render_page_with_shortcode_for_unchanged(self):
        TEST_CASE = ['[/map]xxx[map]',  # wrong order
                     '[map]xxx[/map',   # no end of end tag
                     '[map][/map]',     # empty tag
                     '[map]"[/map]'     # with quote - XSS protection
                     ]
        for item in TEST_CASE:
            self.assertHTMLEqual(render_page_with_shortcode({}, item, safe=True), item)
