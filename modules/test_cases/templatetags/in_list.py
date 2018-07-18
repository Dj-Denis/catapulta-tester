from django import template

register = template.Library()


@register.filter
def in_list(value, list_):
    return str(value) in list_
