from django import forms
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.forms import ChoiceField, MultipleHiddenInput, SelectMultiple
from .models import PlanCases

from .models import Plan


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
