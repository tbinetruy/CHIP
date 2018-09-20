from django.forms.boundfield import BoundField
from django.forms.widgets import Widget, TextInput, CheckboxInput
from django.utils.functional import Promise
from django.utils.html import conditional_escape, format_html
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from chp.components import *
from chp.store import (create_store, render_app)


"""
Boundfield has the following methods to render an HTML widget
using the template engine:
    def __str__(self):
        """ """Render this field as an HTML widget.""" """
        if self.field.show_hidden_initial:
            return self.as_widget() + self.as_hidden(only_initial=True)
        return self.as_widget()

    def as_widget(self, widget=None, attrs=None, only_initial=False):
        """ """
        Render the field by rendering the passed widget, adding any HTML
        attributes passed as attrs. If a widget isn't specified, use the
        field's default widget.
        """ """
        widget = widget or self.field.widget
        if self.field.localize:
            widget.is_localized = True
        attrs = attrs or {}
        attrs = self.build_widget_attrs(attrs, widget)
        if self.auto_id and 'id' not in widget.attrs:
            attrs.setdefault('id', self.html_initial_id if only_initial else self.auto_id)
        return widget.render(
            name=self.html_initial_name if only_initial else self.html_name,
            value=self.value(),
            attrs=attrs,
            renderer=self.form.renderer,
        )

    def build_widget_attrs(self, attrs, widget=None):
        widget = widget or self.field.widget
        attrs = dict(attrs)  # Copy attrs to avoid modifying the argument.
        if widget.use_required_attribute(self.initial) and self.field.required and self.form.use_required_attribute:
            attrs['required'] = True
        if self.field.disabled:
            attrs['disabled'] = True
        return attrs

We need to use similar to get the attrs for 'required', etc.

Alternatively, create custom MdcWidgets and override the widget.render()?

Refactor functions here to classes to support code reuse.
"""

'''
class ChpWidgetMixin:
    chp_widget = None

    def __init__(self, attrs=None, **kwargs):
        self.label = kwargs.pop("label", None)
        if attrs is not None:
            attrs = attrs.copy()
        super().__init__(attrs)

    def render(self, name, value, attrs=None, renderer=None):
        """Build a context and render the widget as a component."""
        context = self.get_context(name, value, attrs)
        context['widget'].update(
            {'label': self.label,
             'id_for_label':
                self.id_for_label(context['widget']['attrs']['id'])
             })
        # return self._render(self.template_name, context, renderer)
        return self.chp_render(context)

    def chp_render(self, context):
        raise NotImplementedError


class MdcCheckboxInput(ChpWidgetMixin, CheckboxInput):

    def chp_render(self, context):
        props = [
            cp("class", "mdc-checkbox"),
            cp("data-mdc-auto-init", "MDCCheckbox"),
        ]
        children = [
            ce("input", [
                cp("id", context['widget']['attrs']['id']),
                cp("type", context['widget']['type']),
                cp("class", "mdc-checkbox__native-control"),
                cp("checked"
                   if context['widget']['attrs']['checked'] else "", ""),
                ],
                []
               ),
            Div([cp("class", "mdc-checkbox__background")],
                []
                ),
        ]
        checkbox = Div(props, children)
        children = [checkbox,
                    MdcLabelWidget(context)
                    ]
        return MdcFormField([], children)
'''

def MdcCheckboxWidget(context):
    props = [
        cp("class", "mdc-checkbox"),
        cp("data-mdc-auto-init", "MDCCheckbox"),
    ]
    children = [
        ce("input", [
            cp("id", context['widget']['attrs']['id']),
            cp("type", context['widget']['type']),
            cp("class", "mdc-checkbox__native-control"),
            cp("checked"
               if context['widget']['attrs']['checked'] else "", ""),
            ],
            []
           ),
        Div([cp("class", "mdc-checkbox__background")],
            []
            ),
    ]
    checkbox = Div(props, children)
    children = [checkbox,
                MdcLabelWidget(context)
                ]
    return MdcFormField([], children)


def MdcCheckbox(field):
    # code taken from Boundfield.label_tag()
    label_suffix = (field.field.label_suffix
                    if field.field.label_suffix is not None
                    else (field.form.label_suffix
                          if hasattr(field, "form") else ""))
    contents = field.label
    if label_suffix and contents and contents[-1] not in _(':?.!'):
        label = format_html('{}{}', contents, label_suffix)

    return field.as_widget()


def MdcFormField(props, children):
    props = [
        cp("class", "mdc-form-field mdc-form-field--align-end"),
        cp("data-mdc-auto-init", "MDCFormField"),
    ]
    return Div(props, children)


def MdcInput(field):
    if field.mdc_type == "MDCDateField":
        input_type = "date"
    else:
        input_type = "text"

    props = [
        cp("type", input_type),
        cp("id", field.auto_id),
        cp("class", "mdc-text-field__input"),
    ]

    # widget formatted value
    value = field.field.widget.format_value(field.value())
    if not (value == '' or value is None):
        props.append(
            cp("value", value)
        )
    # widget-level attrs
    for (key, value) in field.field.widget.attrs.items():
        props.append(
            cp(key, value)
        )

    children = []
    return ce("input", props, children)


def MdcLabel(field):
    props = [
        cp("for", field.id_for_label),
    ]
    if field.mdc_type not in ['MDCCheckbox']:
        props.append(cp("class", "mdc-floating-label"))

    label = field.label
    # cast gettext_lazy strings so they are recognised by AST renderer
    if isinstance(label, Promise):
        label = conditional_escape(label)

    return ce("label", props, label)


def MdcLabelWidget(context):
    props = [
        cp("for", context['widget']['id_for_label']),
    ]
    if context['widget']['type'] not in ['checkbox']:
        props.append(cp("class", "mdc-floating-label"))

    label = context['widget']['label']
    # render gettext_lazy strings so they are recognised by AST renderer
    if isinstance(label, Promise):
        label = str(label)

    return ce("label", props, label)


def MdcLineRipple():
    return Div([cp("class", "mdc-line-ripple")], [])


def MdcTextField(field):
    if not hasattr(field, 'mdc_type'):
        field.mdc_type = 'MDCTextField'
    # ctx = field.field.widget.get_context(field.name, field.value(), None)

    props = [
        cp("class", "mdc-text-field"),
        cp("data-mdc-auto-init", "MDCTextField"),
    ]
    children = [
        MdcInput(field),
        MdcLabel(field),
        MdcLineRipple(),
    ]
    textfield = Div(props, children)
    children = [textfield,
                MdcLabel(field)
                ]
    return MdcFormField([], children)


def MdcDateField(field):
    if not hasattr(field, 'mdc_type'):
        field.mdc_type = 'MDCDateField'
    return MdcTextField(field)


def SubmitButton(name, on_click):
    props = [
        cp('onclick', on_click)
    ]
    return Button(props, name)
