from django import forms
from django.utils.safestring import mark_safe

# from chp import chp
from chp.components import *
from chp.pyreact import (
    context_middleware, inject_ids, render_element
)
from chp.store import (Inject_ast_into_DOM, render_app)

from chp.django.example.todos.components import *


from .models import Post

class PostForm(forms.ModelForm):

    def FormSchema(self, *args, **kwargs):
        # store_name = "todoStore"
        # store_change_cb = [
        #     render_app(store_name, store_content_json),
        # ]
        # 
        # def add_todos():
        #     return f"store_updates.add_todo({store_name})"

        def render():
            form = Form([
                Cell([
                    Div(
                        [cp("style", "display: flex;")],
                        [
                            Input(store_content["name"]),
                            SubmitButton("Submit", add_todos()),
                        ],
                    ),
                    Div(
                        [cp("style", "height: 5rem")],
                        "If you type <strong>foo</strong> in the textbox and unfocus, your secret message will appear !!"
                    ),
                    Div([cp("id", "demo"), cp("style", "color: red" if store_content["name"] == "foo" else "color: green")], "what color am I ?"),
                ])
            ])

            todos = []
            for t in store_content["todos"]:
                todos.append(TodoItem(t["name"], t["id"]))

            return Div(
                [],
                [
                    Script(create_store(store_name, store_change_cb, store_content_json)),
                    form,
                    Div([], todos),
                ],
            )

        return render()

    def render(self):
        import json
        ast = FormSchema(store, json.dumps(store))
        form = inject_ids(ast)
        app = Inject_ast_into_DOM(form, json.dumps(form))
        html = render_element(app, context_middleware(ctx))
        print(html)
        print(form)
        return mark_safe(html)

    class Meta:
        model = Post
        exclude = []
