from django import forms
from django.contrib.auth.forms import UserCreationForm
from user.models import User

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=150, widget=forms.EmailInput(
        attrs={
            'class': 'form-control'
        }

    ))
    password1 = forms.CharField(label='Password', max_length=150, widget=forms.PasswordInput(
        attrs={
            'class': 'form-control'
        }

    ))
    password2 = forms.CharField(label='Verify Password', max_length=150,  widget=forms.PasswordInput(
        attrs={
            'class': 'form-control'
        }

    ))


    class Meta:
        model = User
        fields = (
            #'first_name', 'last_name', 
            
'email', 'password1', 'password2',)