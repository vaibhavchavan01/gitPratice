from django.contrib.auth import get_user_model
from django.contrib.auth import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from django import forms 
class UserCreateForm(UserCreationForm):
    class Meta():
        fields = ('firstname','lastname', 'email','mobile', 'password', 'confirm_password')
        model = User
    
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['username'].label= 'Display Name'
#         self.fields['username'].label = 'Email Address'

class UserForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields = ("email","password")

