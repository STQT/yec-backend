"""
Custom template filters for compatibility with django-jazzmin.
The length_is filter was removed in Django 4.0+ but is still used by jazzmin templates.
"""
from django import template

register = template.Library()


@register.filter
def length_is(value, arg):
    """
    Returns True if the value's length is the argument, False otherwise.
    
    Usage: {{ value|length_is:"5" }}
    """
    try:
        return len(value) == int(arg)
    except (ValueError, TypeError):
        return False

