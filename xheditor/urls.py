from django.conf.urls.defaults import url, patterns

from xheditor.views import xheditor_upload
from xheditor.forms import FileForm, ImageForm


urlpatterns = patterns('',
    url('^upload/image/(?P<upload_to>.*)', xheditor_upload, {
        'form_class': ImageForm,
        'response': lambda name, url: '{"err":"","msg":{"url":"%s","localfile":"%s","id":"1"}}' % (url, name),
        #'response': lambda name, url: '{"err":"","msg":"%s"}' % url,
    }, name='xheditor_upload_image'),

    url('^upload/file/(?P<upload_to>.*)', xheditor_upload, {
        'form_class': FileForm,
        'response': lambda name, url: '<a href="%s">%s</a>' % (url, name),
    }, name='xheditor_upload_file'),
)
