from django import forms
from menuserve.models import Food
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
    

class FoodForm(forms.ModelForm):
    class Meta:
        model = Food
        fields = ('name','price','intro','image')

class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "first_name","last_name")

class LoginForm(forms.Form):
    username = forms.CharField(max_length=50,required=True)
    password = forms.CharField(max_length=50,required=True, widget=forms.PasswordInput)

