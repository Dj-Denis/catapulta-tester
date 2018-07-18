from django.urls import path
from .views import *

urlpatterns = [
    path('plan_list/', PlanList.as_view(), name='plan_list'),
    path('plan_detail/<int:pk>', PlanDetail.as_view(), name='plan_detail'),
    path('plan_create/', PlanCreate.as_view(), name='plan_create'),
    path('plan_edit/<int:pk>', PlanUpdate.as_view(), name='plan_edit'),
    path('plan_delete/<int:pk>', PlanDelete.as_view(), name='plan_delete'),
]
