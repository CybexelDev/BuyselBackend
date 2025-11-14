from django import template

register = template.Library()

@register.filter
def get_by_id(queryset, id_value):
    try:
        return queryset.get(id=id_value)
    except:
        return None
