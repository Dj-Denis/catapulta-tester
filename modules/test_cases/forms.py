from django import forms
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.forms import ChoiceField, MultipleHiddenInput, SelectMultiple

from modules.tags.models import Tag
from modules.tags.models import TaggedItem
from .models import Case


class CustomMultipleChoiceField(ChoiceField):
    hidden_widget = MultipleHiddenInput
    widget = SelectMultiple
    default_error_messages = {
        'invalid_choice': 'Select a valid choice. %(value)s is not one of the available choices.',
        'invalid_list': 'Enter a list of values.',
    }

    def to_python(self, value):
        if not value:
            return []
        elif not isinstance(value, (list, tuple)):
            raise ValidationError(self.error_messages['invalid_list'], code='invalid_list')
        return [str(val) for val in value]

    def validate(self, value):
        """Validate that the input is a list or tuple."""
        if self.required and not value:
            raise ValidationError(self.error_messages['required'], code='required')
        # Validate that each value in the value list is in self.choices.
        for val in value:
            if not self.valid_value(val):
                print(val)
                tag = Tag()
                tag.name = val
                tag.save()


class CaseEditForm(forms.ModelForm):
    tags = CustomMultipleChoiceField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        available_objects = list(Tag.objects.all())
        object_choices = []
        for obj in available_objects:
            obj_id = obj.id
            form_value = str(obj_id)
            display_text = str(obj)
            object_choices.append([form_value, display_text])
        self.fields['tags'].choices = object_choices
        self.fields['tags'].widget.attrs['class'] = 'tags-select'

    def save(self, commit=True):
        object_string = self.cleaned_data['tags']
        case = super().save()
        tagged_items = []
        orig_tagged_items = TaggedItem.objects.filter(content_type=ContentType.objects.get_for_model(Case),
                                                      object_id=case.id)
        for i in object_string:
            try:
                tagged_items.append(TaggedItem.objects.get_or_create(tag=Tag.objects.get(id=i),
                                                                     content_type=ContentType.objects.get_for_model(
                                                                         Case),
                                                                     object_id=case.id)[0])
            except ValueError:
                tagged_items.append(TaggedItem.objects.get_or_create(tag=Tag.objects.get(name=i),
                                                                     content_type=ContentType.objects.get_for_model(
                                                                         Case),
                                                                     object_id=case.id)[0])
        for i in orig_tagged_items:
            if i not in tagged_items:
                i.delete()
        return super(CaseEditForm, self).save()

    class Meta:
        model = Case
        fields = ['name', 'description', 'precondition', 'excepted_result', 'comment', 'tags']
