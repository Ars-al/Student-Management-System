from django import template
import os

register = template.Library()


@register.filter(name='file_name')
def file_name(value):
    return os.path.basename(value)
