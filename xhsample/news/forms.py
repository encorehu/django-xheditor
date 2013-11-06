# -*- coding: utf-8 -*-

# python.
from datetime import datetime
#import urllib
# ------------------------------------------------------------

# django.
from django import forms
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.models import User
# ------------------------------------------------------------

# 3dpart.
#
# ------------------------------------------------------------

from news.models import News,Attachment
from xheditor.widgets import xhEditor
# ------------------------------------------------------------

# config.
# ------------------------------------------------------------



class NewsForm(forms.ModelForm):
    content   = forms.CharField(label=_(u"Content"), widget=xhEditor(attrs={'rows':15, 'cols':66}),required=True)

    class Meta:
        model = News
        exclude = ('deliverer','editor','subtitle','views','comments')

class AttachmentForm(forms.ModelForm):
    file = forms.FileField()

    class Meta:
        model = Attachment
        exclude = ('news','attached_by','attached_at','mimetype','title','slug','description')