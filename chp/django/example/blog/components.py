from chp.components import *
from chp.store import (create_store, render_app)


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
                # MdcLabel(el_id, label, 'MDCTextField')
                MdcLabel(field)
                ]
    return MdcFormField(props, children)


def MdcInput(el_id, value):
    props = [
        cp("type", "text"),
        cp("id", el_id),
        cp("class", "mdc-text-field__input"),
        cp("value", value),
    ]
    children = []
    return ce("input", props, children)


# def MdcLabel(el_id, label, el_type='MDCTextField'):
def MdcLabel(field):
    props = [
        cp("for", field.auto_id),
    ]
    if field.mdc_type not in ['MDCCheckbox']:
        props.append(cp("class", "mdc-floating-label"))

    return ce("label", props, field.label)


def MdcLineRipple():
    return Div([cp("class", "mdc-line-ripple")], [])


def MdcTextField(el_id, label, value):
    props = [
        cp("class", "mdc-text-field"),
        cp("data-mdc-auto-init", "MDCTextField"),
    ]
    children = [
        MdcInput(el_id, value),
        MdcLabel(el_id, label),
        MdcLineRipple(),
    ]
    return Div(props, children)


def SubmitButton(name, on_click):
    props = [
        cp('onclick', on_click)
    ]
    return Button(props, name)
