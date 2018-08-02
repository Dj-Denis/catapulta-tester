from django.conf.urls import url
from django.urls import path

from .views import *

urlpatterns = [
    url(r'^(?P<room_name>[^/]+)/$', room, name='room'),
    path('', ReportList.as_view()),
    path('delete/<int:pk>', ReportDelete.as_view(), name='report_delete'),
]
