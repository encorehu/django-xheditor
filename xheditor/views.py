import os

from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from django.core.files.storage import default_storage
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.core.files.base import ContentFile
from xheditor.forms import ImageForm


UPLOAD_PATH = getattr(settings, 'XHEDITOR_UPLOAD', 'allimgs/')

from news.models import randomfilename

@csrf_exempt
@require_POST
@user_passes_test(lambda u: u.is_staff)
def xheditor_upload(request, upload_to=None, form_class=ImageForm, response=lambda name, url: url):
    for k,v in  request.META.items():
        print k,v
    p,f=request.POST, request.FILES
    #print p
    print f
    form = form_class(request.POST, request.FILES)
    print form.is_valid()
    if form.is_valid():
        file_ = form.cleaned_data['file']
        path = os.path.join(upload_to or UPLOAD_PATH, file_.name)
        real_path = default_storage.save(path, file_)
        print real_path
        return HttpResponse(
            response(file_.name, os.path.join(settings.MEDIA_URL, real_path))
        )
    else:
        # not tested below, because xheditor use ajax upload images.
        if request.META['CONTENT_TYPE']=='application/octet-stream' and request.META['HTTP_CONTENT_DISPOSITION']:
            name     ='namenotset'
            filename ='filenamenotset'
            for x in request.META['HTTP_CONTENT_DISPOSITION'].split(';'):
                if x.strip().startswith('name'):
                    name=x.strip().split('=')[1].strip('\'"')
                if x.strip().startswith('filename'):
                    filename=x.strip().split('=')[1].strip('\'"')

            print filename

            newfilename = randomfilename(filename)
            path = os.path.join(upload_to or UPLOAD_PATH, newfilename)
            image_data = request.raw_post_data # post will equal 'myrawpoststring'
            real_path = default_storage.save(path, ContentFile(image_data))
            print real_path
            return HttpResponse(
                response(filename, os.path.join(settings.MEDIA_URL, real_path))
            )

        return HttpResponse(status=403)
