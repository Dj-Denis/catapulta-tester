from django import template

register = template.Library()


@register.filter
def get_filter_dashboard(filter, table):
    elements = filter.split('?')
    if len(elements) == 2:
        elements = elements[1].split('&')
        for i in elements:
            if table == 'left' and 'page_l' in i:
                elements.pop(elements.index(i))
            elif table == 'right' and 'page_r' in i:
                elements.pop(elements.index(i))
        return '&'.join(elements)
