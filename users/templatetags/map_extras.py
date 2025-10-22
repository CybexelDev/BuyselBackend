# myapp/templatetags/map_extras.py
from django import template
import re

register = template.Library()

@register.filter
def extract_coords(location_url):
    """
    Extract lat,lng from a Google Maps embed URL.
    Returns 'lat,lng' string or empty string if not found.
    """
    match_lat = re.search(r'!3d([-\d\.]+)', location_url)
    match_lng = re.search(r'!2d([-\d\.]+)', location_url)
    if match_lat and match_lng:
        return f"{match_lat.group(1)},{match_lng.group(1)}"
    return ""
