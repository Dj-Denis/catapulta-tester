from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView
from .models import Tag
from django.contrib.contenttypes.models import ContentType
from modules.test_plans.models import Plan


# Create your views here.

class TagsList(ListView):
    model = Tag

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super(TagsList, self).get_context_data(**kwargs)
        counts = []
        for c in ctx['tag_list']:
            counts.append(c.taggeditem_set.filter(content_type=ContentType.objects.get_for_model(Plan)).count())
        ctx.update({'counts': counts})
        return ctx


class TagCreate(CreateView):
    model = Tag
    fields = ('name',)
    success_url = reverse_lazy('tags_list')


class TagDelete(DeleteView):
    model = Tag
    success_url = reverse_lazy('tags_list')
