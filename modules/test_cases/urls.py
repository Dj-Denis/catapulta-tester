from django.urls import path

from .views import *

urlpatterns = [
    path('case_list/', CaseList.as_view(), name='case_list'),
    path('case_detail/<pk>', CaseDetail.as_view(), name='case_detail'),
    path('case_create/', CaseCreate.as_view(), name='case_create'),
    path('case_edit/<int:pk>', CaseUpdate.as_view(), name='case_edit'),
    path('case_delete/<int:pk>', CaseDelete.as_view(), name='case_delete'),
]
