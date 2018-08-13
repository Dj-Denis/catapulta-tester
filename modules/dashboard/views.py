import datetime

import delorean
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.views.generic import ListView

from modules.test_cases.mixins import GroupRequiredMixin
from modules.test_plans.models import Plan


# Create your views here.

class DashboardView(LoginRequiredMixin, GroupRequiredMixin, ListView):
    template_name = 'dashboard/dashboard_list.html'
    model = Plan

    def get_context_data(self, **kwargs):
        date_from = self.request.GET.get('date_from')
        date_to = self.request.GET.get('date_to')
        ctx = super(DashboardView, self).get_context_data(**kwargs)
        ctx['plan_success_count'] = ctx['plan_list'].filter(status='1').count() or 0
        ctx['plan_failed_count'] = ctx['plan_list'].filter(status='2').count() or 0
        ctx['plan_list_before'] = ctx['plan_list']
        if date_from is not None or date_to is not None:
            if len(date_from) != 0 and len(date_to) != 0:
                ctx['plan_list'] = Plan.objects.filter(planlog__last_run__range=[date_from,
                                                                                 delorean.parse(date_to,
                                                                                                dayfirst=False).end_of_day])
                ctx['plan_success_count'] = ctx['plan_list'].filter(status='1').count() or 0
                ctx['plan_failed_count'] = ctx['plan_list'].filter(status='2').count() or 0
                ctx['plan_list_before'] = Plan.objects.filter(
                    planlog__last_run__lte=(
                            delorean.parse(date_from, dayfirst=False) - datetime.timedelta(weeks=4)).end_of_day)
            elif len(date_from) != 0:
                ctx['plan_list'] = Plan.objects.filter(planlog__last_run__range=[date_from, timezone.now()])
                ctx['plan_success_count'] = ctx['plan_list'].filter(status='1').count() or 0
                ctx['plan_failed_count'] = ctx['plan_list'].filter(status='2').count() or 0
                ctx['plan_list_before'] = Plan.objects.filter(
                    planlog__last_run__lte=(
                            delorean.parse(date_from, dayfirst=False) - datetime.timedelta(weeks=4)).end_of_day)
            elif len(date_to) != 0:
                ctx['plan_list'] = Plan.objects.filter(planlog__last_run__range=['1990-1-1',
                                                                                 delorean.parse(date_to).end_of_day])
                ctx['plan_success_count'] = ctx['plan_list'].filter(status='1').count() or 0
                ctx['plan_failed_count'] = ctx['plan_list'].filter(status='2').count() or 0
                ctx['plan_list_before'] = Plan.objects.filter(
                    planlog__last_run__lte=(
                            delorean.parse(date_to, dayfirst=False) - datetime.timedelta(weeks=4)).end_of_day)

        return ctx
