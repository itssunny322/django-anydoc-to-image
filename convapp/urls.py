from django.urls import path
from convapp.views import Fileupload


urlpatterns = [
    path('fileupload/', Fileupload.as_view(), name='task'),
]