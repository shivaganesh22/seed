from django import template

register = template.Library()

@register.filter(name='get_vcodec')
def get_vcodec(value):
    return (value.split('.')[0])[:-1]
@register.filter(name='get_acodec')
def get_acodec(value):
    return value.split('.')[0]