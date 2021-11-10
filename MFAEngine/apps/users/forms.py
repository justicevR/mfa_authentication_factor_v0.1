from django import forms
from apps.users.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import fields
from django.contrib.auth import authenticate



class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=300, help_text='Required.Please enter your first name')
    last_name = forms.CharField(max_length=300, help_text='Required.Please enter your last name')
    email = forms.EmailField(max_length=60, help_text='Required.Please enter your last name')

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2')



class AccountAuthenticationForm(forms.ModelForm):
    password = forms.CharField(label='Password',widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'password')


    def clean(self):
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']
        if not authenticate(email=email, password=password):
            raise forms.ValidationError("Invalid username or password")
            
            