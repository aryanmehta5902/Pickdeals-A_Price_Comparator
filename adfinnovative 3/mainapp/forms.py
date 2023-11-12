from django import forms
from django.forms.widgets import DateInput
from .models import User

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = "__all__"
        widgets = {
            'dob': DateInput(attrs={'type': 'date', 'class': 'custom-date-input'}),
        }
        
class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(max_length=50)
    
class OtpForm(forms.Form):
    verify = forms.CharField(max_length=4) 

class SearchForm(forms.Form):
    instr = forms.CharField(max_length=50, label="Search for a item") 