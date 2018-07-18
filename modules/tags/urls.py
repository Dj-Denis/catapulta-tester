from django.urls import path
from .views import *

urlpatterns = [
    path('tags_list/', TagsList.as_view(), name='tags_list'),
    path('tag_add/', TagCreate.as_view(), name='tag_add'),
    path('tag_delete/<int:pk>', TagDelete.as_view(), name='tag_delete'),
]
