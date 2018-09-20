from django.template import TemplateDoesNotExist, TemplateSyntaxError
from django.template.backends.base import BaseEngine
from django.template.backends.utils import csrf_input_lazy, csrf_token_lazy

from chp.django.example.blog.components import MdcCheckboxWidget

class ComponentEngine(BaseEngine):

    # Name of the subdirectory containing the templates for this engine
    # inside an installed application.
    app_dirname = 'components'


    #  dict of template path -> component
    template_components = {
        'django/forms/widgets/checkbox.html': MdcCheckboxWidget,
    }

    def __init__(self, params=None):
        super().__init__(dict(
            NAME='chp',
            DIRS=[],
            APP_DIRS=True,
        ))

    def from_string(self, template_code):
        """
        This would enable::

            django.template.render('''
                <chp.django.MdcCheckBox id="the-id" value="" />
            ''')
        """
        raise NotImplemented()

    def get_template(self, template_name):
        # one day maybe: support dotted import path ie.:
        # django.template.render('chp.django.SomeComponent')

        # immediate objective is to map django templates to components
        # to help migration of existing django code, particularely in the case
        # of forms that's the immediate goal

        if template_name not in self.template_components:
            from django.forms.renderers import DjangoTemplates
            try:
                return DjangoTemplates().get_template(template_name)
            except:
                raise TemplateDoesNotExist(template_name, backend=self)

        component = self.template_components[template_name]
        return Template(component)

        ''' from django docs:
        try:
            return Template(template_name)
        except foobar.TemplateNotFound as exc:
            raise TemplateDoesNotExist(exc.args, backend=self)
        except foobar.TemplateCompilationFailed as exc:
            raise TemplateSyntaxError(exc.args)
        '''

    def render(self, template_name, context, request=None):
        template = self.get_template(template_name)
        return template.render(context, request=request).strip()


class Template:

    def __init__(self, template):
        self.template = template

    def render(self, context=None, request=None):
        return self.template(context)
        '''
        if context is None:
            context = {}
        if request is not None:
            context['request'] = request
            context['csrf_input'] = csrf_input_lazy(request)
            context['csrf_token'] = csrf_token_lazy(request)
        return self.template.render(context)
        '''
