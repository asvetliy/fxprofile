from django import template

register = template.Library()


@register.filter
def get_at_index(l, index):
    return l[index-1]
