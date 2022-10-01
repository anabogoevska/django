from dataclasses import Field

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class RegisterForm(forms.ModelForm):

    class Meta:
        model = User
        exclude=("user",)

        widgets ={

     'first_name': forms.TextInput(attrs={'class': 'form-control'}),
     'last_name': forms.TextInput(attrs={'class': 'form-control'}),
     'email': forms.TextInput(attrs={'class': 'form-control'}),
      'username': forms.TextInput(attrs={'class': 'form-control'}),
      'password': forms.TextInput(attrs={'class': 'form-control'}),

        }

class IndexForm(UserCreationForm):
        email = forms.EmailField()
        first_name=forms.CharField(max_length=150)
        last_name = forms.CharField(max_length=150)

        class Meta:
             model = User
             fields = ("first_name", "last_name", 'username','email',"password1", "password2")

class MyAuthenticationForm(AuthenticationForm):
    username = forms.CharField(max_length=150)
    password = forms.CharField(max_length=12)

    widgets = {
    'username': forms.TextInput(attrs={'class': 'form-control'}),
    'password': forms.TextInput(attrs={'class': 'form-control'}),
    }