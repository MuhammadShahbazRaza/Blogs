from django import template
from django.utils.text import Truncator

register = template.Library()

@register.filter
def truncatelines(value, lines):
    truncator = Truncator(value)
    return truncator.words(lines, html=True, truncate=' ...')