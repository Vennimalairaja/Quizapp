from django import forms
from .models import Questions
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Staff
class QuestionForm(forms.ModelForm):
    class Meta:
        model=Questions
        fields='__all__'

class StaffUserCreationForm(UserCreationForm):
    class Meta:
        model=User
        fields=['username','email','password1','password2']
