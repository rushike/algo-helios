from django import template
import jinja2
register = template.Library()

@register.simple_tag
def define(val=None):
  return val

@register.filter(name='_replace')
def _replace(val=None, args = " "):
  args = args.split("??")
  ini = args[0]
  aft = args[1]
  return val.replace(ini, aft)

@register.filter(name='_split')
def _split(val="None", args = " "):
  args = args.split("??")
  index = int(args[0])
  char = args[1]
  return val.split(char)[index]

