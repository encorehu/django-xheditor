# -*- coding: utf-8 -*-

# python.
#import datetime
#import urllib
# ------------------------------------------------------------

# django.
from django.contrib import admin
from django.core.urlresolvers import reverse
from django import forms
from django.template import Template, Context, RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
# ------------------------------------------------------------

# 3dpart.
#
# ------------------------------------------------------------

# ddtcms.
from news.models import News
from news.models import Attachment
from news.forms import NewsForm
# ------------------------------------------------------------

# config.
#FIELD_MAX_LENGTH = getattr(settings, 'FIELD_MAX_LENGTH', 100)
#n_dict={
#"sitename":"Example",
#}
# ------------------------------------------------------------


class NewsAdmin(admin.ModelAdmin):

    def save_model(self, request, obj, form, change):
        instance = form.save(commit=False)
        instance.deliverer = request.user
        instance.editor    = request.user.username
        instance.save()
        form.save_m2m()
        instance.check_content_attachments()
        return instance

    list_display = ('title', 'slug','deliverer','pub_date','status')
    list_filter = ['pub_date','status']
    form = NewsForm



class AttachmentAdmin(admin.ModelAdmin):
    list_display = ('news', 'title','file')


admin.site.register(News,NewsAdmin)
admin.site.register(Attachment,AttachmentAdmin)
