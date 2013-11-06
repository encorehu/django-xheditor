# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# Script   Name: models.py
# Creation Date: 2011-11-05  02:22
# Last Modified: 2011-11-12 17:19:35
# Copyright (c)2011, DDTCMS Project
# Purpose: This file used for DDTCMS Project
# ------------------------------------------------------------

# python.
import datetime
import os
import re
import random
import mimetypes
# ------------------------------------------------------------

# django.
from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.utils import encoding
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.utils import timezone
# ------------------------------------------------------------

# 3dpart.
# ------------------------------------------------------------

# project.
def randomfilename(filename):
	if len(filename)>0:
		base, ext = os.path.splitext(filename)
		if not ext:
		    ext = '.jpg'
		ran_filename = datetime.datetime.now().strftime("%Y%m%d%H%M%S") + str(random.randrange(0, 100, 2)).rjust(2,'0') + random.choice('abcdefghijklmnopqrstuvwxyz')
		ran_filename = "%s%s" % (ran_filename , ext)
		return ran_filename.lower()
	else:
		return datetime.datetime.now().strftime("%Y%m%d%H%M%S") + str(random.randrange(0, 100, 2)).rjust(2,'0') +".tmp"

# Get relative media path
try:
    ATTACHMENT_DIR = settings.ATTACHMENT_DIR
except:
    ATTACHMENT_DIR = "allimgs"

# Look for user function to define file paths
def get_storage_path(instance, filename):
    return os.path.join(ATTACHMENT_DIR, randomfilename(filename))
# ------------------------------------------------------------

# config.
#FIELD_MAX_LENGTH = getattr(settings, 'FIELD_MAX_LENGTH', 100)
#n_dict={
#"sitename":"Example",
#}
# ------------------------------------------------------------



NEWS_STATUS = (
(0,  _('NORMAL')),
(1,  _('HEADLINE')),
(2,  _('RECOMMENDED')),
(3,  _('FLASHSLIDE')),
(9,  _('DELETED')),
)

class News(models.Model):
    deliverer      = models.ForeignKey(User,verbose_name='Deliverer',null=True,editable=True)
    title          = models.CharField(max_length=200)
    slug           = models.SlugField(max_length=255,blank=True,unique=True,help_text='Automatically built From the title.')
    pub_date       = models.DateTimeField('date published',blank=True,default=timezone.now)
    content        = models.TextField()
    summary        = models.TextField(help_text="Summary",null=True,blank=True)
    views          = models.PositiveIntegerField(_("Views"), default=0)
    comments       = models.PositiveIntegerField(_("Comments"), default=0)
    allow_comments = models.BooleanField(_("Allow Comments"),default=True)
    approved       = models.BooleanField(_("Approved"),default=True)
    pic            = models.CharField('News Indicator Pic',max_length=200,null=True,blank=True,help_text="If has a pic url,show on homepage or indexpage")
    status         = models.PositiveIntegerField(_("Status"), choices=NEWS_STATUS, default=0)

    class Meta:
        ordering            = ('-pub_date',)
        unique_together     = (('slug', 'pub_date'), )
        get_latest_by       = 'pub_date'
        verbose_name        = _('News')
        verbose_name_plural = _('News')

    def get_absolute_url(self):
        return "/news/detail/%d/" % self.id

    def __unicode__(self):
        return self.title

    def _get_pic_url(self):
        """This gets the tag list for the news"""
        if not hasattr(self, '__pic_url'):
            self.__pic_url = self.pic
            if not self.__pic_url:
                self.__pic_url = '/media/allimgs/noimg.jpg'

        return self.__pic_url
    pic_url = property(_get_pic_url)

    def total_attachments(self):
        return self.attachment_set.count()

    def get_content_pic_urls(self):
        pattern= 'src\=[\"\']?(/media/([/\w]+)\.(jpg|png|gif|jpeg|bmp))[\"\']?'
        p = re.compile(pattern)

        find_parts = p.findall(self.content)
        pic_urls =list()
        for x in find_parts:
            pic_urls.append(x[0])
        self.pic_urls=pic_urls
        return pic_urls

    def get_pic_url(self):
        self.pic_urls = self.get_content_pic_urls()
        if self.pic_urls:
            return self.pic_urls[0]
        else:
            return None

    def check_content_attachments(self, upload_session=None):
        pic_urls = self.get_content_pic_urls()
        for pic_url in pic_urls:
            pic_url = pic_url.replace(settings.MEDIA_URL, '')
            if pic_url=='':
                continue

            try:
                attachment = Attachment.objects.filter(file = pic_url).latest('attached_at')
            except Attachment.DoesNotExist:
                attachment = Attachment()
                attachment.file = pic_url

            if not attachment.news_id: # if not saved
                attachment.news = self
                attachment.title = self.title
                attachment.attached_by = self.deliverer
                attachment.save()

    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            self.slug = self.slug.lower().replace('-','_')

        if not self.pic:
            self.pic = self.get_pic_url()

        super(News,self).save(*args,**kwargs)
        self.check_content_attachments()

class Attachment(models.Model):
    news        = models.ForeignKey(News, null=True, blank=True)
    attached_by = models.ForeignKey(User, related_name="attachment_attached_by", editable=False)
    attached_at = models.DateTimeField("Date attached", default=timezone.now)
    file        = models.FileField(upload_to=get_storage_path)
    mimetype    = models.CharField(editable=False, max_length=100)
    title       = models.CharField(max_length=200, null=True, blank=True)
    slug        = models.SlugField(editable=False, null=True, blank=True)
    description = models.TextField(max_length=255, null=True, blank=True)

    class Meta:
        ordering = ['-attached_at']
        get_latest_by = 'attached_at'

    def __unicode__(self):
        return self.title

    def save(self, force_insert=False, force_update=False):
        file_path = '%s%s' % (settings.MEDIA_ROOT, self.file.name)

        if not self.title:
            self.title = u'\u4e0a\u4f20\u6587\u4ef6'

        (mime_type, _encoding) = mimetypes.guess_type(file_path)
        try:
            self.mimetype = mime_type
        except:
            self.mimetype = 'text/plain'
        super(Attachment, self).save(force_insert, force_update)


    def file_url(self):
        return encoding.iri_to_uri(self.file.url)

    def mime_type(self):
        return '%s' % self.mimetype

    def type_slug(self):
        return slugify(self.mimetype.split('/')[-1])

    def is_image(self):
    	file_type=self.mimetype.split('/')[0]
        if file_type == 'image':
            return True
        else:
            return False

    def get_absolute_url(self):
		return '%s%s' % (settings.MEDIA_URL, self.file.url)

    def delete(self, *args, **kwargs):
        # http://stackoverflow.com/questions/5372934/how-do-i-get-django-admin-to-delete-files-when-i-remove-an-object-from-the-datab
        # You have to prepare what you need before delete the model
        storage, path = self.file.storage, self.file.path
        # Delete the model before the file
        super(Attachment, self).delete(*args, **kwargs)
        # Delete the file after the model
        storage.delete(path)