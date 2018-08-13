from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView

from modules.test_cases.mixins import GroupRequiredMixin
from .models import Tag


# Create your views here.

class TagsList(LoginRequiredMixin, GroupRequiredMixin, ListView):
    model = Tag
    paginate_by = 25


class TagCreate(LoginRequiredMixin, GroupRequiredMixin, CreateView):
    model = Tag
    fields = ('name',)
    success_url = reverse_lazy('tags_list')


class TagDelete(LoginRequiredMixin, GroupRequiredMixin, DeleteView):
    model = Tag
    success_url = reverse_lazy('tags_list')
