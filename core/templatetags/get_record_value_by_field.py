from django.template import Library

register = Library()

@register.filter
def get_record_value_by_field(value, field):
    return getattr(value, field)