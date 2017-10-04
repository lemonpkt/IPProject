from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UsernameField


class UserForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput)


    class Meta:
        model=User
        fields=['username','email','password','first_name','last_name']


class LoginForm(AuthenticationForm):
    username = UsernameField(
        widget=forms.TextInput()
    )
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input', 'placeholder': 'password'}))
