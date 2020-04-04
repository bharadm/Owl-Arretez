from django import template

register = template.Library()


@register.filter
def get_key(value):
    return value["question"]


@register.filter
def get_var(value):
    return value["answer"]