from django import template

register = template.Library()

@register.filter
def find(value, arg):
    return value.find(arg)

@register.filter
def split_name_voucher(value, arg):
    value.split("arg")
    return value.split(arg)[1]

@register.filter
def subtract(value, arg):
    return value - arg

@register.filter(name='multiplication') # nhân
def multiplication(value, arg):
    return value * arg