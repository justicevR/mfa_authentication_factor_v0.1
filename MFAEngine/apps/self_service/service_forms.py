from apps.self_service.models import ApplicationRequest
from django import forms
from django.db.models import fields
from ..api import models
#from api.models import App
#from users.models import User


class RegisterAppForm(forms.ModelForm):
    name_of_app = forms.CharField(max_length=255, help_text='Required.Please enter the name of your applications')
    domain = forms.CharField(max_length=100, help_text='Required.Please enter the domain for your application')
    org_name = forms.CharField(max_length=200, help_text='Required.Please enter the name of the organization of your application')
    redirect_uris = forms.CharField(max_length=400,help_text='Required.Please enter redirect uris for your app')
    claim_of_property = forms.CharField(max_length=400, help_text='Required.Please provide the proof of property')


    class Meta:
        model = ApplicationRequest
        fields = ('name_of_app', 'domain', 'org_name', 'redirect_uris' , 'claim_of_property')


class InviteAppForm(forms.ModelForm):

    class Meta:
        model = models.App
        fields = '__all__'
 
        