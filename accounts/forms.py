from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms

from django.core.exceptions import ValidationError

from accounts.models import Profile


class MyUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        fields = ['username', 'password1', 'password2', 'first_name', 'last_name', 'email']

    def clean(self):
        if not (self.cleaned_data.get('first_name') or self.cleaned_data.get('last_name')):
            raise ValidationError('Укажите либо имя, либо фамилию')
        return super().clean()


class UserChangesForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'email']
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'email': 'Email'
        }


class ProfileChangesForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'github_profile', 'description']
