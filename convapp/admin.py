from django.contrib import admin
from .models import FileModel,ImgModel
# Register your models here.

admin.site.register(FileModel)
admin.site.register(ImgModel)