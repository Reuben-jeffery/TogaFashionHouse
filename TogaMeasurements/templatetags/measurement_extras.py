from django import template

register = template.Library()

@register.filter
def attr(obj, attr_name):
    """Allows dynamic attribute access in templates: {{ object|attr:"field_name" }}"""
    return getattr(obj, attr_name, None)
