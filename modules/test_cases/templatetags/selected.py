from django import template
from django.utils.html import format_html

register = template.Library()


@register.simple_tag
def selected(objects, sel):
    resp = ''
    for obj in objects:
        if str(obj.pk) in sel:
            resp += '<option value="{}" selected>{}</option>'.format(obj.pk, obj.name)
        else:
            resp += '<option value="{}">{}</option>'.format(obj.pk, obj.name)
    return format_html(resp)
