from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic import ListView, DeleteView
from django.views.generic import UpdateView

from .forms import (AccountEditForm,
                    CustomUserCreationForm,
                    GroupEditForm,
                    GroupCreateForm,
                    AccountAddForm,
                    AdminAccountEditForm,
                    )
from .models import Account, CustomGroup


# Create your views here.

class AccountsList(LoginRequiredMixin, ListView):
    model = Account
    template_name = 'account/account_list.html'


class AccountSettings(LoginRequiredMixin, UpdateView):
    model = Account
    template_name = 'account/account_form.html'
    # success_url = reverse_lazy('dashboard')
    form_class = AccountEditForm
    # form_class = AccountEditForm

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


class AccountDelete(LoginRequiredMixin, DeleteView):
    model = Account
    success_url = reverse_lazy('account_list')


class Registration(CreateView):
    model = Account
    template_name = 'account/registration_form.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('dashboard')


class GroupList(LoginRequiredMixin, ListView):
    model = CustomGroup
    template_name = 'account/groups_list.html'


class GroupCreate(LoginRequiredMixin, CreateView):
    model = CustomGroup
    # fields = ['name']
    form_class = GroupCreateForm
    template_name = 'account/group_form.html'
    success_url = reverse_lazy('groups_list')


class GroupEdit(LoginRequiredMixin, UpdateView):
    model = CustomGroup
    template_name = 'account/group_form.html'
    success_url = reverse_lazy('groups_list')
    # fields = ['name', 'permissions']
    form_class = GroupEditForm


class GroupDelete(LoginRequiredMixin, DeleteView):
    model = CustomGroup
    # template_name = 'account/group_form.html'
    success_url = reverse_lazy('groups_list')
