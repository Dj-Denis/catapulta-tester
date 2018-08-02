import json

from django.shortcuts import render
from django.utils.safestring import mark_safe
from django.views.generic import ListView, DeleteView

# Create your views here.
from .models import Report


class ReportList(ListView):
    model = Report


class ReportDelete(DeleteView):
    model = Report


def room(request, room_name):
    return render(request, 'report/chat.html', {
        'room_name_json': mark_safe(json.dumps(room_name))
    })
