from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UsernameField
from .models import UserProfile


class UserForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput)


    class Meta:
        model= UserProfile
        fields=['username','email','password','first_name','last_name','Identification']


class LoginForm(AuthenticationForm):
    username = UsernameField(
        widget=forms.TextInput()
    )
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input', 'placeholder': 'password'}))
