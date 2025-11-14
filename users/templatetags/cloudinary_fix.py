from django import template

register = template.Library()

@register.filter
def cloudinary_og(url):
    """Insert f_auto,q_auto for OG sharing"""
    if not url:
        return url
    return url.replace("/upload/", "/upload/f_auto,q_auto/")
