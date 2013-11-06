# -*- coding: utf-8 -*-

# python.
#import datetime
# ------------------------------------------------------------

# django.
from django.conf.urls.defaults import *
from django.views.generic import DetailView, ListView

# ------------------------------------------------------------

# 3dpart.
# ------------------------------------------------------------

# ddtcms.
from news.models import News
from news.views  import NewsDetailView
# ------------------------------------------------------------

# config.
#FIELD_MAX_LENGTH = getattr(settings, 'FIELD_MAX_LENGTH', 100)
try:
    PAGINATE = settings.NEWS_PAGINATE_BY
except:
    PAGINATE = 10

# ------------------------------------------------------------



urlpatterns = patterns('',

    url(r'^detail/(?P<pk>\d+)/$',
        DetailView.as_view(
            model=News,

        ),
        name='news_detail'
    ),

    url(r'^post/$','news.views.post', name='news_post'),

    url(r'^$', ListView.as_view(model=News), name='news_index'),
)