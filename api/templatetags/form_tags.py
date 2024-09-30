# api/templatetags/form_tags.py

from django import template

register = template.Library()

@register.filter(name='add_class')
def add_class(field, css_class):
    """
    Adds the specified CSS class to the form field's widget.
    """
    return field.as_widget(attrs={"class": css_class})