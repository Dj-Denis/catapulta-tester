import datetime

import delorean
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.utils import timezone
from django.views.generic import ListView

from modules.test_cases.mixins import GroupRequiredMixin
from modules.test_plans.models import Plan


# Create your views here.

class DashboardView(LoginRequiredMixin, GroupRequiredMixin, ListView):
    template_name = 'dashboard/dashboard_list.html'
    model = Plan
    paginate_by = 10

    def get_context_data(self, **kwargs):
        date_from = self.request.GET.get('date_from')
        date_to = self.request.GET.get('date_to')
        ctx = super(DashboardView, self).get_context_data(**kwargs)
        # ctx['plan_success_count'] = ctx['plan_list'].filter(status='1').count() or 0
        # ctx['plan_failed_count'] = ctx['plan_list'].filter(status='2').count() or 0
        ctx['plan_list_before'] = ctx['plan_list']
        q_list_l = []
        q_list_r = []
        if date_from is not None or date_to is not None:

            if len(date_from) != 0 and len(date_to) != 0:
                q_list_r.append(Q(planlog__last_run__range=[date_from, delorean.parse(date_to, dayfirst=False).end_of_day]))
                ctx['plan_success_count'] = ctx['plan_list'].filter(status='1').count() or 0
                ctx['plan_failed_count'] = ctx['plan_list'].filter(status='2').count() or 0
                q_list_l.append(Q(planlog__last_run__lte=(delorean.parse(date_from, dayfirst=False)
                                                          - datetime.timedelta(weeks=4)).end_of_day))
            elif len(date_from) != 0:
                q_list_r.append(Q(planlog__last_run__range=[date_from, timezone.now()]))
                ctx['plan_success_count'] = ctx['plan_list'].filter(status='1').count() or 0
                ctx['plan_failed_count'] = ctx['plan_list'].filter(status='2').count() or 0
                q_list_l.append(Q(
                    planlog__last_run__lte=(
                            delorean.parse(date_from, dayfirst=False) - datetime.timedelta(weeks=4)).end_of_day))
            elif len(date_to) != 0:
                q_list_r.append(Q(planlog__last_run__range=['1990-1-1',
                                                                                 delorean.parse(date_to).end_of_day]))
                ctx['plan_success_count'] = ctx['plan_list'].filter(status='1').count() or 0
                ctx['plan_failed_count'] = ctx['plan_list'].filter(status='2').count() or 0
                q_list_r.append(Q(
                    planlog__last_run__lte=(
                            delorean.parse(date_to, dayfirst=False) - datetime.timedelta(weeks=4)).end_of_day))
        table_l = Plan.objects.filter(*q_list_l)
        table_r = Plan.objects.filter(*q_list_r)

        paginator_l = Paginator(table_l, self.paginate_by)
        paginator_r = Paginator(table_r, self.paginate_by)
        page_l = self.request.GET.get('page_l')
        page_r = self.request.GET.get('page_r')

        try:
            table_r = paginator_r.page(page_r)
        except PageNotAnInteger:
            table_r = paginator_r.page(1)
        except EmptyPage:
            table_r = paginator_r.page(paginator_r.num_pages)
        ctx['plan_list'] = table_r
        ctx['paginator_r'] = paginator_r

        try:
            table_l = paginator_l.page(page_l)
        except PageNotAnInteger:
            table_l = paginator_l.page(1)
        except EmptyPage:
            table_l = paginator_l.page(paginator_l.num_pages)
        ctx['plan_list_before'] = table_l
        ctx['paginator_l'] = paginator_l
        return ctx
