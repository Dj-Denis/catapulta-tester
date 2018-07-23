from django import template

register = template.Library()


@register.filter
def in_queryset(qs_):
    pr = [i[0] for i in qs_.values_list('provider')]
    return pr
