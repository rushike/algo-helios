from django import template
import jinja2
register = template.Library()
@register.simple_tag
def _split(val=None, index = 0, char = " "):
  return val.split(char)[index]
