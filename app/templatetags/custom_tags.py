from django import template

register = template.Library()

@register.filter(name='get_vcodec')
def get_vcodec(value):
    return (value.split('.')[0])[:-1]
@register.filter(name='get_acodec')
def get_acodec(value):
    return value.split('.')[0]
@register.filter(name='get_last_update')
def get_last_update(value):
    sorted_data = sorted(value, key=lambda x: x['last_update'],reverse=True)
    return sorted_data
