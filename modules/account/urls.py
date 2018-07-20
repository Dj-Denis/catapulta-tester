from django.urls import path

from .views import *

urlpatterns = [
    path('accounts_list/', AccountsList.as_view(), name='account_list'),
    path('account_edit/<int:pk>', AccountSettings.as_view(), name='account_edit'),
    path('account_register/', Registration.as_view(), name='register'),
    path('account_add/', AccountAdd.as_view(), name='account_add'),
    path('account_delete/<int:pk>', AccountDelete.as_view(), name='account_delete'),
    path('groups_list/', GroupList.as_view(), name='groups_list'),
    path('group_create/', GroupCreate.as_view(), name='group_create'),
    path('group_edit/<int:pk>', GroupEdit.as_view(), name='group_edit'),
    path('group_delete/<int:pk>', GroupDelete.as_view(), name='group_delete'),

]
