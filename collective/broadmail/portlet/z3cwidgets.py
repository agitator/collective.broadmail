from zope.interface import implementsOnly
from z3c.form import field
from z3c.form import form
from z3c.form.interfaces import IWidgets
from z3c.form.interfaces import IForm


class EmptyPrefixFieldWidgets(field.FieldWidgets):
    """Override default Field Widgets to get rid of prefix"""
    implementsOnly(IWidgets)
    prefix = ''


class EmptyPrefixForm(form.BaseForm):
    """Override default Form to get rid of prefix"""
    implementsOnly(IForm)
    prefix = ''
