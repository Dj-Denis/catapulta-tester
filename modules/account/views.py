from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic import ListView, DeleteView
from django.views.generic import UpdateView

from modules.test_cases.mixins import GroupRequiredMixin
from .forms import (AccountEditForm,
                    CustomUserCreationForm,
                    GroupEditForm,
                    GroupCreateForm,
                    AccountAddForm,
                    AdminAccountEditForm,
                    )
from .models import Account, CustomGroup


# Create your views here.

class AccountsList(LoginRequiredMixin, GroupRequiredMixin, ListView):
    model = Account
    template_name = 'account/account_list.html'
    paginate_by = 50


class AccountSettings(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Account
    template_name = 'account/account_form.html'
    form_class = AccountEditForm
    success_message = "Настройки успешно сохранены"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if self.request.user.is_admin:
            return super(AccountSettings, self).dispatch(request, *args, **kwargs)
        elif self.request.path_info.split('/')[3] != str(self.request.user.id):
            return redirect(self.request.user)
        else:
            return super(AccountSettings, self).dispatch(request, *args, **kwargs)

    def get_form_class(self):
        if self.request.user.is_admin:
            return AdminAccountEditForm
        else:
            return AccountEditForm


class AccountAdd(LoginRequiredMixin, CreateView):
    model = Account
    template_name = 'account/account_add.html'
    form_class = AccountAddForm
    success_url = reverse_lazy("account_list")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_admin:
            return super(AccountAdd, self).dispatch(request, *args, **kwargs)
        else:
            return self.handle_no_permission()


class AccountDelete(LoginRequiredMixin, DeleteView):
    model = Account
    success_url = reverse_lazy('account_list')
    permission_denied_message = ''

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_admin:
            return super(AccountDelete, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied()


class Registration(CreateView):
    model = Account
    template_name = 'account/registration_form.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('dashboard')


class GroupList(LoginRequiredMixin, GroupRequiredMixin, ListView):
    model = CustomGroup
    template_name = 'account/groups_list.html'


class GroupCreate(LoginRequiredMixin, CreateView):
    model = CustomGroup
    # fields = ['name']
    form_class = GroupCreateForm
    template_name = 'account/group_form.html'
    success_url = reverse_lazy('groups_list')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_admin:
            return super(GroupCreate, self).dispatch(request, *args, **kwargs)
        else:
            return self.handle_no_permission()


class GroupEdit(LoginRequiredMixin, UpdateView):
    model = CustomGroup
    template_name = 'account/group_form.html'
    success_url = reverse_lazy('groups_list')
    # fields = ['name', 'permissions']
    form_class = GroupEditForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_admin:
            return super(GroupEdit, self).dispatch(request, *args, **kwargs)
        else:
            return self.handle_no_permission()


class GroupDelete(LoginRequiredMixin, DeleteView):
    model = CustomGroup
    # template_name = 'account/group_form.html'
    success_url = reverse_lazy('groups_list')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_admin:
            return super(GroupDelete, self).dispatch(request, *args, **kwargs)
        else:
            return self.handle_no_permission()
