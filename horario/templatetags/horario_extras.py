from datetime import timedelta

from django import template

register = template.Library()

@register.filter
def soma_dia(value, args):
    if args == 'SEG':
        args = 0
    if args == 'TER':
        args = 1
    if args == 'QUA':
        args = 2
    if args == 'QUI':
        args = 3
    if args == 'SEX':
        args = 4
    if args == 'SAB':
        args = 5
    return value + timedelta(days=args)

@register.filter
def soma_semana(value, args):
    return value + timedelta(days=args*7)