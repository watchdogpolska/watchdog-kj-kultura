import re

from django import template
from django.utils.html import mark_safe, escape

register = template.Library()

RE_MAP = re.compile(r'\[map\](.+)\[\/map\]', re.DOTALL)


def repl(match):
    return '<div class="map">%s</div>' % (match.group(1))


@register.simple_tag(takes_context=True)
def render_page_with_shortcode(context, value, safe=False):
    """The function to essential render text of static pages with shortcodes.

    Replace occurences of [map]x[/map] to HTML code. Decorated with ``register.simple_tag``.

    Parameters
    ----------
    context : dict
        context of template
    value : a string to render
        A string to render
    safe : bool, optional
        Treat input as safe

    Returns
    -------
    str -- rendered
    """

    if safe is False:
        value = escape(value)
    return mark_safe(RE_MAP.sub(repl, value))
