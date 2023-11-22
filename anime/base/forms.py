from django.forms import ModelForm
from .models import User, Customer
from django.contrib.auth.forms import UserCreationForm
from django import forms

class MyUserCreationForm(UserCreationForm):

    class Meta:
        model= User
        fields= ['name','email','avatar','gender','newslatter','password1','password2']
        
        
class UserForm(ModelForm):
    class Meta:
        model= User
        fields=['avatar','name','bio','gender','address','phone','newslatter']


#Samin Rahman
class RegistrationForm(forms.Form):
    email_address = forms.EmailField(label='Your email address')
    phone_number = forms.IntegerField(label='Please enter your phone number')

