from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from django.forms import TextInput,FileInput,Select,EmailInput,PasswordInput

from home.models import UserProfile

class UserUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')
        widgets = {
                  'username' : TextInput(attrs={'class': 'form-control', 'placeholder': 'username'}),
                  'email': EmailInput(attrs={'class': 'form-control', 'placeholder': 'email'}),
                  'first_name': TextInput(attrs={'class': 'form-control', 'placeholder': 'first_name'}),
                  'last_name': TextInput(attrs={'class': 'form-control', 'placeholder': 'last_name'}),
        }

CITY = [
        ('Istanbul', 'Istanbul'),
        ('Ankara', 'Ankara'),
        ('Izmir', 'Izmir'),
]
#Profile update form allows users to image
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('ogrencino', 'phone', 'address', 'city', 'country', 'image')
        widgets = {
                  'ogrencino':TextInput(attrs={'class': 'form-control', 'placeholder': 'ogrencino'}),
                  'phone': TextInput(attrs={'class': 'form-control', 'placeholder': 'phone'}),
                  'address': TextInput(attrs={'class': 'form-control', 'placeholder': 'address'}),
                  'city': Select(attrs={'class': 'form-control', 'placeholder': 'city'}, choices=CITY),
                  'country': TextInput(attrs={'class': 'form-control', 'placeholder': 'country'}),
                  'image': FileInput(attrs={'class': 'form-control', 'placeholder': 'image'}),
        }