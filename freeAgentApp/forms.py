from django import forms
from django.contrib.auth.forms import AuthenticationForm, UsernameField
from .models import UserProfile


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'Identification']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }


class LoginForm(AuthenticationForm):
    username = UsernameField(
        widget=forms.TextInput()
    )
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input'}))
