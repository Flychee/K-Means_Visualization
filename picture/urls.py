from . import views
from django.urls import re_path as url

urlpatterns = [
    url(r'^$', views.picture, name='index'),
]