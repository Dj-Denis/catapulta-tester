from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import View
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import CreateView
from django.views.generic.edit import DeleteView
from django.views.generic.edit import UpdateView
from djqscsv import render_to_csv_response

from modules.account.models import Account
from modules.test_cases.mixins import GroupRequiredMixin
from modules.test_cases.models import Case
from .forms import PlanUpdateForm, PlanLogForm
from .models import Plan, PlanLog


# Create your views here.


class PlanList(LoginRequiredMixin, GroupRequiredMixin, ListView):
    model = Plan
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super(PlanList, self).get_context_data(**kwargs)
        ctx['accounts_list'] = Account.objects.all()
        req = self.request.GET.dict()
        if 'page' in req:
            del req['page']
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
            paginator = Paginator(resp, self.paginate_by)
            page = self.request.GET.get('page')
            try:
                _resp = paginator.page(page)
            except PageNotAnInteger:
                _resp = paginator.page(1)
            except EmptyPage:
                _resp = paginator.page(paginator.num_pages)
            ctx['plan_list'] = _resp
            ctx['paginator'] = paginator
        return ctx


class PlanDetail(LoginRequiredMixin, GroupRequiredMixin, DetailView):
    model = Plan

    def get_context_data(self, **kwargs):
        ctx = super(PlanDetail, self).get_context_data(**kwargs)
        ctx['cases'] = Case.objects.filter(plan=self.object).order_by('pk')
        ctx['logs'] = PlanLog.objects.filter(plan=self.object).order_by('-last_run')
        return ctx


class PlanCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Plan
    permission_required = 'add_plan'
    fields = ['name', 'description']

    def form_valid(self, form):
        form.instance.create_by = self.request.user
        form.save()
        return super(PlanCreate, self).form_valid(form)


class PlanUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Plan
    permission_required = 'change_plan'
    # fields = ['name', 'description']
    form_class = PlanUpdateForm


class PlanDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Plan
    permission_required = ['delete_plan']
    success_url = reverse_lazy('plan_list')


class CSVExportView(SingleObjectMixin, View):
    model = Plan

    def get(self, request, *args, **kwargs):
        return render_to_csv_response(Case.objects.filter(plancases__plan_id=self.get_object().pk).all())


class PlanRun(LoginRequiredMixin, GroupRequiredMixin, CreateView):
    model = PlanLog
    form_class = PlanLogForm
    # success_url = reverse_lazy('plan_log')

    def get_context_data(self, **kwargs):
        data = super(PlanRun, self).get_context_data(**kwargs)
        return data

    def get_initial(self):
        initial = super(PlanRun, self).get_initial()
        initial['id'] = self.request.GET.get('plan_id')
        return initial

    def form_valid(self, form):
        form.instance.create_by = self.request.user
        return super(PlanRun, self).form_valid(form)


class PlanLogDetail(LoginRequiredMixin, GroupRequiredMixin, DetailView):
    model = PlanLog
