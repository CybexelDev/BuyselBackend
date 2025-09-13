
from django import template

register = template.Library()

@register.filter
def dict_lookup(d, key):
    """Safely lookup a dictionary value in Django templates"""
    if isinstance(d, dict):
        return d.get(key, 0)
    return 0
