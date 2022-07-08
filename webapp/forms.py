from django import forms
from django.forms import widgets

from webapp.models import Status, Type


class IssueForm(forms.Form):
    summary = forms.CharField(max_length=50, label='Краткое описание')
    description = forms.CharField(max_length=3000, required=False, label='Полное описание', widget=widgets.Textarea())
    status = forms.ModelChoiceField(queryset=Status.objects.all())
    type = forms.ModelChoiceField(queryset=Type.objects.all())