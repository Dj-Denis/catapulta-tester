from crispy_forms.bootstrap import (FormActions, Div)
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field, HTML
from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.forms import UserCreationForm
from django.forms.widgets import FileInput
from image_cropping import ImageCropWidget
from registration.forms import RegistrationFormUniqueEmail

from .models import Account, CustomGroup


class AccountEditForm(UserChangeForm):
    email = forms.CharField(label="Почтовый адрес", required=True)
    password1 = forms.CharField(label='Пароль', required=False, widget=forms.PasswordInput)
    password2 = forms.CharField(label='Подтверждение пароля', required=False, widget=forms.PasswordInput)
    first_name = forms.CharField(label="Имя", required=False, disabled=True)
    second_name = forms.CharField(label="Фамилия", required=False, disabled=True)
    avatar = forms.ImageField(label="", required=False, widget=FileInput)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        if len(password1) != 0 and len(password2) != 0:
            password_validation.validate_password(password1)
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        if len(self.cleaned_data["password1"]) != 0:
            user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

    def __init__(self, *args, **kwargs):
        super(AccountEditForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.layout = Layout(
            Div(Div(Field('email', css_class='input-sm', ),
                    Field('first_name', css_class='input_sm'),
                    Field('second_name', css_class='input_sm'),
                    HTML("<div>Роли:</div>"
                         "{% for group in object.groups.all %}"
                         "<div class='ml-2'> {{ group.name }} </div>"
                         "{% endfor %}"),
                    Field('password1', css_class='input-sm'),
                    Field('password2', css_class='input-sm'),
                    FormActions(Submit('submit', 'Сохранить', css_class='btn-primary'), css_class=''),
                    css_class='col-6'),
                Div(Field(HTML('<img src="{{ object.avatar.url }}" style="width: 200px; height:200px;" class="mb-3"/>'
                               '<p><small>Максимальный размер картинки 400х400px</small></p>'),
                          'avatar'),
                    css_class='col-6 text-center'),
                css_class='row')
        )

    class Meta:
        model = Account
        fields = ['email', 'password', 'avatar', 'first_name', 'second_name']
        widgets = {
            "avatar": ImageCropWidget
        }


class AdminAccountEditForm(UserChangeForm):
    email = forms.CharField(label="Почтовый адрес", required=True)
    password1 = forms.CharField(label='Пароль', required=False, widget=forms.PasswordInput)
    password2 = forms.CharField(label='Подтверждение пароля', required=False, widget=forms.PasswordInput)
    first_name = forms.CharField(label="Имя", )
    second_name = forms.CharField(label="Фамилия")
    avatar = forms.ImageField(label="", required=False, widget=FileInput)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        if len(password1) != 0 and len(password2) != 0:
            password_validation.validate_password(password1)
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        if len(self.cleaned_data["password1"]) != 0:
            user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

    def __init__(self, *args, **kwargs):
        super(AdminAccountEditForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.layout = Layout(
            Div(Div(Field('email', css_class='input-sm', ),
                    Field('first_name', css_class='input_sm'),
                    Field('second_name', css_class='input_sm'),
                    Field('group'),
                    Field('is_active', template='account/select.html'),
                    Field('password1', css_class='input-sm'),
                    Field('password2', css_class='input-sm'),
                    FormActions(Submit('submit', 'Сохранить', css_class='btn-primary'), css_class=''),
                    css_class='col-6'),
                Div(Field(HTML('<img src="{{ object.avatar.url }}" style="width: 200px; height:200px;" class="mb-3"/>'
                               '<p><small>Максимальный размер картинки 400х400px</small></p>'),
                          'avatar'),
                    css_class='col-6 text-center'),
                css_class='row')
        )

    class Meta:
        model = Account
        fields = ['email', 'password', 'avatar', 'first_name', 'second_name', 'group', 'is_active']
        widgets = {
            "avatar": ImageCropWidget
        }


class AccountRegisterForm(UserCreationForm):
    email = forms.CharField(label="Почтовый адрес", required=True)
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput)
    first_name = forms.CharField(label="Имя", required=True)
    second_name = forms.CharField(label="Фамилия", required=True)
    avatar = forms.ImageField(label="", required=False, widget=FileInput)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")

        password_validation.validate_password(password1)
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

    def __init__(self, *args, **kwargs):
        super(AccountRegisterForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.layout = Layout(
            Div(Div(Field('email', css_class='input-sm', ),
                    Field('first_name', css_class='input_sm'),
                    Field('second_name', css_class='input_sm'),
                    Field('password1', css_class='input-sm'),
                    Field('password2', css_class='input-sm'),
                    FormActions(Submit('submit', 'submit', css_class='btn-primary'), css_class=''),
                    css_class='col-6'),
                Div(Field(HTML(
                    '<img src="/media/avatars/default-user.png" style="width: 200px; height:200px;" class="mb-3"/>'),
                    'avatar'),
                    css_class='col-6 text-center'),
                css_class='row')
        )

    class Meta:
        model = Account
        fields = ['email', 'password', 'avatar', 'first_name', 'second_name']


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Account
        fields = ('email', 'first_name', 'second_name')


class GroupCreateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(GroupCreateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.layout = Layout(
            Field('name'),
            FormActions(Submit('submit', 'Подтвердить', css_class='btn-primary btn-success'), css_class='mt-3'),
        )

    class Meta:
        model = CustomGroup
        fields = ('name',)


class GroupEditForm(forms.ModelForm):
    name = forms.CharField(label="Название", required=True)
    permissions = forms.CheckboxSelectMultiple()

    def __init__(self, *args, **kwargs):
        super(GroupEditForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.layout = Layout(
            Field('name'),
            Field('permissions', template='account/switch.html'),
            FormActions(Submit('submit', 'Подтвердить', css_class='btn-primary btn-success'), css_class='mt-3'),
        )

    class Meta:
        model = CustomGroup
        fields = ('name', 'permissions')
        widgets = {
            'permissions': forms.CheckboxSelectMultiple(),
        }


class AccountAddForm(UserCreationForm):
    password1 = forms.CharField(
        label="Пароль",
        strip=False,
        widget=forms.PasswordInput,
    )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
            super()._save_m2m()
        return user

    class Meta:
        model = Account
        fields = ('email', 'first_name', 'second_name', 'group')


class CustomRegistrationForm(RegistrationFormUniqueEmail):
    password1 = forms.CharField(
        label="Пароль",
        strip=False,
        widget=forms.PasswordInput,
    )
    password2 = forms.CharField(
        label="Подтверждение пароля",
        widget=forms.PasswordInput,
        strip=False,
    )

    class Meta:
        model = Account
        fields = ("email", 'first_name', 'second_name')