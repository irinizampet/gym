from django import template

register = template.Library()

@register.filter
def mul(value, arg):
    """
    Πολλαπλασιάζει value * arg.
    Παράδειγμα: {{ 10|mul:5 }} => 50
    """
    try:
        return value * arg
    except Exception:
        return ''
