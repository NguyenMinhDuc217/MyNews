from django import forms
from . import models
from django.core.validators import RegexValidator
# from django.contrib.auth.models import User

phone_validator = RegexValidator(r"((\([0-9]{3}\)[0-9]{9,15})|([0-9]{10,15}))","Your phone number must be (xxx)xxxxxxxxx or 0xxxxxxxx!")
class UserForm(forms.ModelForm):
    password = forms.CharField(max_length=150, label='Password', widget=forms.PasswordInput(attrs={
        'placeholder':'Enter your password aa',
        'class':'form-control'
        }))
    confirm = forms.CharField(max_length=150, label='Confirm', widget=forms.PasswordInput(attrs={
        'placeholder':'Confirm your password',
        'class':'form-control'
        }))
    class Meta:
        model = models.User
        fields = ('username','email','password','first_name','last_name')

class UserProfileInfoForm(forms.ModelForm):
    address = forms.CharField(max_length=150, label='Address', widget=forms.TextInput(attrs={
        'placeholder':'Enter your address',
        'class':'form-control'
        }))
    phoneNumber = forms.CharField(max_length=20, label='Phone', validators=[phone_validator], widget=forms.TextInput(
        attrs={
        'placeholder':'Enter your phone',
        'class':'form-control',
        'pattern':'((\([0-9]{3}\)[0-9]{9,15})|([0-9]{10,15}))',
        'title':'Your phone number must be (xxx)xxxxxxxxx or 0xxxxxxxx!'
        }
    ))
    image = forms.ImageField(required=False)
    class Meta:
        model = models.UserProfileInfo
        exclude = ('user',)