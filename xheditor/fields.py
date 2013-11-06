#-*- coding: utf-8 -*-
from django.db.models import Field
from xheditor.widgets import xhEditor


class xhEditorField(Field):
    def __init__(self, *args, **kwargs):
        options = kwargs.pop('xheditor_options', {})
        upload_to = kwargs.pop('upload_to', '')
        self.widget = xhEditor(xheditor_options=options, upload_to=upload_to)
        super(xhEditorField, self).__init__(*args, **kwargs)

    def get_internal_type(self):
        return "TextField"

    def formfield(self, **kwargs):
        defaults = {'widget': self.widget}
        defaults.update(kwargs)
        return super(xhEditorField, self).formfield(**defaults)

try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ['^xheditor\.fields\.xhEditorField'])
except ImportError:
    pass
