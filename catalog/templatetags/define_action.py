from django import template
import jinja2
register = template.Library()

@register.simple_tag
def define(val=None):
  	return val

@register.filter(name='_replace')
def _replace(val=None, args = " "):
	args = args.split("??")
	return val.replace(args[0], args[1])

@register.filter(name='_split')
def _split(val="None", args = " "):
	args = args.split("??")
	index = int(args[0])
	char = args[1]
	return val.split(char)[index]
  

@register.filter(name='_space')
def _space(val="None", args = 10):
	le = len(val)
	half = int((args - le) / 2)
	
	return (" " * half) + val + (" " * half) + " -"

