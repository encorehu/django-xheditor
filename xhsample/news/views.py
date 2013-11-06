# -*- coding: utf-8 -*-

# python.
import datetime
# ------------------------------------------------------------

# django.
from django.shortcuts import render_to_response
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _

# django::decrators
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView

# ------------------------------------------------------------

# 3dpart.
# ------------------------------------------------------------

# ddtcms.
from news.models import News
from news.forms  import NewsForm
from news.models import Attachment
# ------------------------------------------------------------

# config.
#
# ------------------------------------------------------------

class NewsDetailView(DetailView):

    model               = News
    context_object_name = 'news'
    template_name       = 'news/news_detail.html'

    def get_object(self):
        # Call the superclass
        object = super(NewsDetailView, self).get_object()
        # Record the last accessed date
        object.views += 1
        object.save()
        # Return the object
        return object

from xheditor.forms import ImageForm
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
@login_required
def post(request, category = "", success_url=None,
             form_class=NewsForm,
             template_name='news/news_post.html',
             extra_context=None):

    if request.method == 'POST':
        form = form_class(data=request.POST, files=request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.deliverer = request.user
            instance.save()
            form.save_m2m()

            instance.check_content_attachments() # check attachments in the content, and save to attachment table

            return HttpResponseRedirect(instance.get_absolute_url())
    else:
        initial={
            'deliverer':request.user.id,
        }
        form = form_class(initial=initial)

    if extra_context is None:
        extra_context = {}
    context = RequestContext(request)
    for key, value in extra_context.items():
        context[key] = callable(value) and value() or value
    return render_to_response(template_name,
                              { 'form': form,
                              },
                              context_instance=context)
