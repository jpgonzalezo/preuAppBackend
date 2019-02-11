from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^region$',views.RegionList.as_view()),
    url(r'region/(?P<pk>[0-9]+)$',views.RegionDetail.as_view()),
]
