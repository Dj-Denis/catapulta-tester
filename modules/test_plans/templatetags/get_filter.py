from django import template

register = template.Library()


@register.filter
def get_filter(filter):
    elements = filter.split('?')
    if len(elements) == 2:
        elements = elements[1].split('&')
        for i in elements:
            if 'page' in i:
                elements.pop(elements.index(i))
        return '&'.join(elements)
    else:
        return ''
