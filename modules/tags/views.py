from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView

from modules.test_cases.mixins import GroupRequiredMixin
from modules.test_plans.models import Plan
from .models import Tag


# Create your views here.

class TagsList(LoginRequiredMixin, GroupRequiredMixin, ListView):
    model = Tag

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super(TagsList, self).get_context_data(**kwargs)
        counts = []
        for c in ctx['tag_list']:
            counts.append(c.taggeditem_set.filter(content_type=ContentType.objects.get_for_model(Plan)).count())
        ctx.update({'counts': counts})
        return ctx


class TagCreate(LoginRequiredMixin, GroupRequiredMixin, CreateView):
    model = Tag
    fields = ('name',)
    success_url = reverse_lazy('tags_list')


class TagDelete(LoginRequiredMixin, GroupRequiredMixin, DeleteView):
    model = Tag
    success_url = reverse_lazy('tags_list')
