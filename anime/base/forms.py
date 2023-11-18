from django.forms import ModelForm
from .models import User
from django.contrib.auth.forms import UserCreationForm


class MyUserCreationForm(UserCreationForm):

    class Meta:
        model= User
        fields= ['name','email','avatar','gender','newslatter','password1','password2']
        
        
class UserForm(ModelForm):
    class Meta:
        model= User
        fields=['avatar','name','bio','gender','newslatter']