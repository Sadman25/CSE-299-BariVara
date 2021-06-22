from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

# Form for user signup
class UserSignUpForm(UserCreationForm):
    email= forms.EmailField()

    class Meta:
        model=User
        fields= ['username', 'email', 'password1', 'password2']


# Form for upadating user info in Profile feature
class UserUpdateForm(forms.ModelForm):
    email= forms.EmailField()

    class Meta:
        model=User
        fields= ['username', 'email']


#Form for updating image in Profile
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model=Profile
        fields=['image']