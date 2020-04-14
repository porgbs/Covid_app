from __future__ import unicode_literals
from django.db import models
from filer.models import File
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver
import os
from django.conf import settings
import uuid
import ffmpeg


# Create your models here.
class Video(File):
    _icon = 'video'
    file_type = 'video'

    @classmethod
    def matches_file_type(cls, iname, ifile, request):
        filename_extensions = ['.dv', '.mov', '.mp4', '.avi', '.wmv', ]
        ext = os.path.splitext(iname)[1].lower()
        return ext in filename_extensions


@receiver(models.signals.post_save, sender=Video)
def do_generate_thumbnail(sender, instance, created, **kwargs):
    path = instance.url
    source = path.split('/')[-1]
    path_source_v0 = path.replace(source, '')
    path_source_v1 = path_source_v0.replace('/media', 'media')
    source_name = source.split('.')[0]

    full_path = os.path.join(settings.BASE_DIR, path_source_v1 + source)
    target_file = os.path.join(settings.BASE_DIR, path_source_v1 + source_name + ".jpg")
    os.system('ffmpeg -i {0} -ss 00:00:2 -vframes 1 -f image2 {1}'.format(full_path, target_file))
