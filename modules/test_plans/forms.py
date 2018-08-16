from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Field, Submit, HTML
from django import forms
from django.utils import timezone

from modules.test_cases.models import Case
from modules.test_cases.models import CaseLog
from .models import Plan, PlanLog
from .models import PlanCases


class PlanUpdateForm(forms.ModelForm):
    # cases = forms.CheckboxSelectMultiple(attrs={'required': False})
    cases = forms.ModelMultipleChoiceField(required=False, queryset=Case.objects.all())

    # forms.

    def __init__(self, *args, **kwargs):
        super(PlanUpdateForm, self).__init__(*args, **kwargs)
        self.fields['cases'].widget.attrs['class'] = 'searchable'
        self.fields['cases'].widget.attrs['required'] = False
        print(self.fields['cases'].widget.attrs)

    def save(self, commit=True):
        plan = super().save(commit=False)

        orig_cases = PlanCases.objects.filter(plan=plan)
        new_cases = []
        cases = self.cleaned_data.get('cases')

        for case in cases:
            new_cases.append(PlanCases.objects.get_or_create(plan=plan, case=case)[0])
        plan.save()

        for i in orig_cases:
            if i not in new_cases:
                i.delete()

        return plan

    class Meta:
        model = Plan
        fields = ['name', 'description', 'cases']


class CustomCheckboxSelectMultiple(forms.CheckboxSelectMultiple):
    template_name = 'account/switch.html'


class PlanLogForm(forms.ModelForm):
    comment = forms.CharField(widget=forms.Textarea, label='Коментарий к плану', required=False)

    def is_valid(self):
        return self.is_bound

    def save(self, commit=True):
        if self.errors:
            raise ValueError(
                "The %s could not be %s because the data didn't validate." % (
                    self.instance._meta.object_name,
                    'created' if self.instance._state.adding else 'changed',
                )
            )

        planlog = PlanLog()
        planlog.plan_id = self.plan_id
        planlog.comment = self.cleaned_data.get('comment')
        planlog.run_by = self.instance.create_by
        planlog.save()
        for case in self.cases:
            case_id = case.case_id
            case_status = self.cleaned_data.get('case_status_%s' % case_id)
            # if self.cleaned_data.get('case_status_%s' % case_id):
            #     case_status = 1
            # else:
            #     case_status = 0
            case_comment = self.cleaned_data.get('case_comment_%s' % case_id)
            CaseLog(case_id=case_id, comment=case_comment,
                    plan_run_log=planlog, run_by=self.instance.create_by, status=int(case_status)).save()
            _case = case.case
            _case.status = case_status
            _case.last_run = timezone.now()
            print(_case)
            _case.save()
            if case_status == 0:
                planlog.status = 0
                planlog.save()
                plan = Plan.objects.get(pk=self.plan_id)
                print(0)
                plan.status = 2
                plan.last_run = timezone.now()
                plan.save()
            else:
                planlog.status = 1
                planlog.save()
                plan = Plan.objects.get(pk=self.plan_id)
                print(1)
                plan.status = 1
                plan.last_run = timezone.now()
                plan.save()

        return planlog

    def __init__(self, *args, **kwargs):
        super(PlanLogForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.plan_id = self.initial['id']
        plan = Plan.objects.get(pk=self.plan_id)
        self.cases = plan.plancases_set.all()
        self.helper.layout = Layout()
        for case in self.cases:
            self.fields['case_status_%s' % case.case_id] = forms.BooleanField(label='Выполнено', required=False)
            self.fields['case_comment_%s' % case.case_id] = forms.CharField(widget=forms.Textarea, max_length=300,
                                                                            label='Коментарий',
                                                                            required=False)

            self.helper.layout.append(
                Div(HTML("<a class='text-dark' href='%s' ><h5 class='card_title'>%s</h5></a>" % (
                    case.case.get_absolute_url(), case.case.name)),
                    HTML("<p class='card-subtitle mb-2 text-muted'>Описание:</p>"),
                    HTML("<p class=card-text>%s</p>" % case.case.description),
                    HTML("<p class='card-subtitle mb-2 text-muted'>Предварительные условия:</p>"),
                    HTML("<p class=card-text>%s</p>" % case.case.precondition),
                    HTML("<p class='card-subtitle mb-2 text-muted'>Ожидаемый результат:</p>"),
                    HTML("<p class='card-text'>%s</p>" % case.case.excepted_result),
                    Div(Field('case_status_%s' % case.case_id, template='account/select.html'),
                        Field('case_comment_%s' % case.case_id, css_class='planrun__comment-case'),
                        css_class='planrun_card-body'), css_class='planrun__card'), )

        self.helper.layout.append(Div(Field('comment'), FormActions(Submit('submit', 'Сохранить',
                                                                           css_class='btn-primary ml-3')),
                                      css_class='planrun__comment'))

    class Meta:
        model = PlanLog
        fields = ['comment']
