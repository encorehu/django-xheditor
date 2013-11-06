# -*- coding: utf-8 -*-

# python.
#import datetime
#import urllib
# ------------------------------------------------------------

# django.
from django import forms
from django.conf import settings
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _
# ------------------------------------------------------------

EDITOR_VERSION="1.1.12"

class xhEditor(forms.Textarea):

    class Media:
        js  = (
                # 1.1.12
                'xheditor-%s/jquery/jquery-1.4.4.min.js'  % EDITOR_VERSION,
                'xheditor-%s/xheditor-%s-zh-cn.min.js' % (EDITOR_VERSION,EDITOR_VERSION),
        )

    def __init__(self, *args, **kwargs):
        self.upload_to = kwargs.pop('upload_to', '')
        super(xhEditor, self).__init__(*args, **kwargs)

    def get_options(self):
        options = GLOBAL_OPTIONS.copy()
        options.update(self.custom_options)
        options.update({
            'imageUpload': reverse('xheditor_upload_image', kwargs={'upload_to': self.upload_to}),
            'fileUpload': reverse('xheditor_upload_file', kwargs={'upload_to': self.upload_to})
        })
        return json.dumps(options)

    def render(self, name, value, attrs=None):
        rendered = super(xhEditor, self).render(name, value, attrs)
        context = {
            'name': name,
            'STATIC_URL':settings.STATIC_URL,
            'uploadimgurl':reverse('xheditor_upload_image', kwargs={'upload_to': self.upload_to}),
        }
        return rendered  + mark_safe(render_to_string('xheditor/xheditor.html', context))