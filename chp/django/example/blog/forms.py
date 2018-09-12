from django import forms
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

# from chp import chp
from chp.components import *
from chp.pyreact import (
    context_middleware, inject_ids, render_element
)
from chp.store import (create_store, Inject_ast_into_DOM, render_app)

from chp.django.example.blog.components import *

from .components import (MdcCheckbox, MdcTextField)
from .models import Post


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = "__all__"
        labels = {
            'checkbox': _("This is my checkbox"),
            'text': _("Input Label")}

    def FormSchema(self, *args, **kwargs):
        # store_name = "todoStore"
        # store_change_cb = [
        #     render_app(store_name, store_content_json),
        # ]
        # 
        # def add_todos():
        #     return f"store_updates.add_todo({store_name})"

        def render(self, *args, **kwargs):

            form = Form([
                Cell([
                    Div(
                        [cp("style", "display: flex;")],
                        [
                            MdcCheckbox(self["checkbox"]),
                            MdcTextField(self["text"]),
                            # MdcDateField(self.fields["date"]),
                            # MdcSelect(self.fields["foreignkey"]),
                        ],
                    ),
                ])
            ])

            return Div(
                [],
                    # output = super(ModelForm, self).render(value)
                [
                    # Script(create_store(store_name,
                    #                     store_change_cb,
                    #                     store_content_json)),
                    form,
                    # Div([], todos),
                ],
            )

        return render(self)

    def render(self):

        ctx = {}  # perhaps a hidden field on the form?

        ast = self.FormSchema()
        form = inject_ids(ast, context_middleware(ctx))
#         app = Inject_ast_into_DOM(form, json.dumps(form))
#         html = render_element(app, context_middleware(ctx))
        html = render_element(form, context_middleware(ctx))

        return mark_safe(html)
