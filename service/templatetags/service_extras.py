from django.template import Library


register = Library()

@register.filter
def model_type(value):
    return type(value).__name__

@register.filter(name='range')
def filter_range(start, end):
    if isinstance(end, str):
        end_nb = int(end)
    else:
        end_nb = end
    return range(start, end_nb)

@register.filter(name='get_range')
def get_range(value):
    return range(value)

@register.filter(name='get_complement_range')
def get_complement_range(value):
    return range(5 - value)

@register.filter
def add_class(field, css_class):
    return field.as_widget(attrs={'class': css_class})
