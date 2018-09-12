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


def MdcFormField(props, children):
    props = [
        cp("class", "mdc-form-field mdc-form-field--align-end"),
        cp("data-mdc-auto-init", "MDCFormField"),
    ]
    return Div(props, children)


def MdcCheckbox(field):
    field.mdc_type = 'MDCCheckbox'

    props = [
        cp("class", "mdc-checkbox"),
        cp("data-mdc-auto-init", "MDCCheckbox"),
    ]
    children = [
        ce("input", [
            cp("id", field.auto_id),
            cp("type", "checkbox"),
            cp("class", "mdc-checkbox__native-control"),
            cp("checked" if field.value() else "", ""),
            ],
            []
           ),
        Div([cp("class", "mdc-checkbox__background")],
            []
            ),
    ]
    print(field.value())
    checkbox = Div(props, children)
    children = [checkbox,
                MdcLabel(field)
                ]
    return MdcFormField(props, children)


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
        cp("for", field.auto_id),
    ]
    if field.mdc_type not in ['MDCCheckbox']:
        props.append(cp("class", "mdc-floating-label"))

    # cast gettext_lazy strings so they are recognised by AST renderer
    return ce("label", props, str(field.label))


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
    return Div(props, children)


def MdcDateField(field):
    if not hasattr(field, 'mdc_type'):
        field.mdc_type = 'MDCDateField'
    return MdcTextField(field)


def SubmitButton(name, on_click):
    props = [
        cp('onclick', on_click)
    ]
    return Button(props, name)
