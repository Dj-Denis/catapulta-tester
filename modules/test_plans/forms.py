from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Field, Fieldset, Submit
from django import forms

from modules.test_cases.models import CaseLog
from .models import Plan, PlanLog
from .models import PlanCases


class PlanUpdateForm(forms.ModelForm):
    cases = forms.CheckboxSelectMultiple()

    def __init__(self, *args, **kwargs):
        super(PlanUpdateForm, self).__init__(*args, **kwargs)
        self.fields['cases'].widget.attrs['class'] = 'searchable'

    def save(self, commit=True):
        plan = super().save(commit=False)
        print(plan)

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
    id = forms.IntegerField(label='')

    # def clean(self):
    #     # print('2')
    #     return
    #
    def is_valid(self):
        print(self.errors)
        return self.is_bound

    def save(self, commit=True):
        planlog = PlanLog()
        planlog.plan_id = self.plan_id
        planlog.comment = self.cleaned_data.get('comment')
        planlog.run_by = self.instance.create_by
        planlog.save()
        print(self.cases)
        for case in self.cases:
            case_id = case.case_id
            case_status = self.cleaned_data.get('case_status_%s' % case_id)
            case_comment = self.cleaned_data.get('case_comment_%s' % case_id)
            print(case_id)
            print(case_comment)
            CaseLog(case_id=case_id, comment=case_comment,
                        plan_run_log=planlog, run_by=self.instance.create_by, status=int(case_status)).save()
            case.status = case_status
            case.save()
            if not case_status:
                planlog.status = int(case_status)
                planlog.save()

        return planlog

    def __init__(self, *args, **kwargs):
        super(PlanLogForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.fields['id'].widget.attrs['class'] = 'd-none'
        self.plan_id = self.initial['id']
        plan = Plan.objects.get(pk=self.plan_id)
        self.cases = plan.plancases_set.all()
        self.helper.layout = Layout()
        for case in self.cases:
            self.fields['case_status_%s' % case.case_id] = forms.BooleanField(label='Выполнено', required=False)
            self.fields['case_comment_%s' % case.case_id] = forms.CharField(max_length=300, label='Коментарий',
                                                                       required=False)

            self.helper.layout.append(
                Div(Fieldset(case.case.name, Field('case_status_%s' % case.case_id, template='account/select.html'),
                             Field('case_comment_%s' % case.case_id, css_class='planrun__comment-case')), css_class='planrun__card'),)

        self.helper.layout.append(Div(Field('comment'), FormActions(Submit('submit', 'Сохранить',
                                                                           css_class='btn-primary ml-3')),
                                      css_class='planrun__comment'))

    class Meta:
        model = PlanLog
        fields = ['comment', 'id']
