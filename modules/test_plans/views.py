import operator
from functools import reduce

from django.db.models import Q
from django.utils import timezone
from django.views.generic import ListView
from django.views.generic import DetailView
from .models import Plan, PlanLog
from modules.test_cases.models import Case
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from modules.account.models import Account
import delorean

from .forms import PlanUpdateForm

# Create your views here.


class PlanList(ListView):
    model = Plan

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super(PlanList, self).get_context_data(**kwargs)
        ctx['accounts_list'] = Account.objects.all()
        req = self.request.GET.dict()
        if len(req) != 0:
            q_list = []
            if req['search_string'] != '':
                q_list.append(Q(name=req['search_string']))
            if req['result'] != '':
                q_list.append(Q(status=req['result']))
            if req['run_by'] != '':
                q_list.append(Q(planlog__run_by_id__exact=req['run_by']))
            if req['date_from'] != '':
                q_list.append(Q(planlog__last_run__gte=req['date_from']))
            if req['date_to'] != '':
                q_list.append(Q(planlog__last_run__lte=req['date_to'] + ' 23:59:59'))
            resp = Plan.objects.filter(*q_list).distinct()
            ctx['plan_list'] = resp
        return ctx


class PlanDetail(DetailView):
    model = Plan

    def get_context_data(self, **kwargs):
        ctx = super(PlanDetail, self).get_context_data(**kwargs)
        ctx['cases'] = Case.objects.filter(plan=self.object)
        ctx['logs'] = PlanLog.objects.filter(plan=self.object)
        return ctx


class PlanCreate(LoginRequiredMixin, CreateView):
    model = Plan
    fields = ['name', 'description']

    def form_valid(self, form):
        form.instance.create_by = self.request.user
        form.save()
        return super(PlanCreate, self).form_valid(form)


class PlanUpdate(LoginRequiredMixin, UpdateView):
    model = Plan
    # fields = ['name', 'description']
    form_class = PlanUpdateForm


class PlanDelete(LoginRequiredMixin, DeleteView):
    model = Plan
    success_url = reverse_lazy('plan_list')
