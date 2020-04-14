from __future__ import unicode_literals
from django.contrib import admin
from core.admin import BaseModelAdmin
from .models import Video

# Register your models here.
admin.site.register(Video, BaseModelAdmin)
