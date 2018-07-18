from django.db.models import Q
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Case
from django.contrib.contenttypes.models import ContentType
from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from .forms import CaseEditForm
from modules.tags.models import TaggedItem, Tag
from modules.account.models import Account
from modules.test_plans.models import Plan
from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator


# Create your views here.

class CaseList(ListView):
    model = Case

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super(CaseList, self).get_context_data(**kwargs)
        ctx['accounts_list'] = Account.objects.all()
        ctx['plan_list'] = Plan.objects.all()
        ctx['tag_list'] = Tag.objects.all()
        req = self.request.GET.dict()
        selected_tags = self.request.GET.getlist('tags')
        ctx['selected_tags'] = selected_tags
        if len(req) != 0:
            q_list = []
            whit_tags = []
            if req['search_string'] != '':
                q_list.append(Q(name=req['search_string']))
            if req['result'] != '':
                q_list.append(Q(status=req['result']))
            if req['run_by'] != '':
                q_list.append(Q(caselog__run_by_id__exact=req['run_by']))
            if req['date_from'] != '':
                q_list.append(Q(last_run__gte=req['date_from']))
            if req['date_to'] != '':
                q_list.append(Q(last_run__lte=req['date_to'] + ' 23:59:59'))
            if req['plan'] != '':
                q_list.append(Q(plancases__plan_id=req['plan']))
            for selected_tag in selected_tags:
                filter_tagged = TaggedItem.objects.filter(content_type=ContentType.objects.get_for_model(Case),
                                                          tag_id__exact=selected_tag)
                whit_tags.extend([item[0] for item in filter_tagged.values_list('object_id')])
            if len(whit_tags) != 0:
                q_list.append(Q(pk__in=set(whit_tags)))

            resp = Case.objects.filter(*q_list).distinct()
            ctx['case_list'] = resp
        return ctx


class CaseDetail(DetailView):
    model = Case

    def get_context_data(self, **kwargs):
        ctx = super(CaseDetail, self).get_context_data(**kwargs)
        ctx['tags'] = TaggedItem.objects.filter(content_type=ContentType.objects.get_for_model(self.model),
                                                object_id=self.object.pk)
        return ctx


class CaseCreate(LoginRequiredMixin, CreateView):
    model = Case
    # form_class = CaseEditForm
    fields = ['name', 'description', 'precondition', 'excepted_result', 'comment']

    def form_valid(self, form):
        form.instance.create_by = self.request.user
        form.save()
        return super(CaseCreate, self).form_valid(form)


class CaseUpdate(LoginRequiredMixin, GroupRequiredMixin, UpdateView):
    model = Case
    form_class = CaseEditForm
    permission_required = 'edit_case'
    permission_denied_message = 'Вы не имеете права делать это'
    raise_exception = True

    def get_initial(self):
        initial = super(CaseUpdate, self).get_initial()
        tags = TaggedItem.objects.filter(content_type=ContentType.objects.get_for_model(self.model),
                                         object_id=self.get_object().id).values_list('tag_id', flat=True)
        initial['tags'] = list(tags)
        return initial


class CaseDelete(LoginRequiredMixin, DeleteView):
    model = Case
    success_url = reverse_lazy('case_list')
