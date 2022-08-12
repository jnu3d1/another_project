from django import forms
from django.core.exceptions import ValidationError
from django.forms import widgets

from webapp.models import Issue, Project


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'users', 'start_date', 'end_date']
        widgets = {
            'description': widgets.Textarea,
            'users': widgets.CheckboxSelectMultiple,
            'start_date': widgets.SelectDateWidget,
            'end_date': widgets.SelectDateWidget
        }


class IssueForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = ['summary', 'description', 'status', 'types']
        widgets = {
            'description': widgets.Textarea,
            'types': widgets.CheckboxSelectMultiple
        }

    def clean_summary(self):
        summary = self.cleaned_data.get('summary')
        if len(summary) > 50:
            raise ValidationError('Краткое описание не должно превышать 50 символов!')
        return summary

    def clean_description(self):
        description = self.cleaned_data.get('description')
        if len(description) > 50:
            raise ValidationError('Полное описание не должно превышать 3000 символов!')
        return description

    def clean(self):
        if self.cleaned_data.get('summary') == self.cleaned_data.get('description'):
            raise ValidationError('Полное описание не должно копировать краткое')
        return super().clean()


class SearchForm(forms.Form):
    search = forms.CharField(label='Поиск', max_length=50, required=False)
