from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import *


from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class User_form(UserCreationForm):

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")

        return password2

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'address', 'password1', 'password2']  # Include password1 and password2

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}), 
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}), 
            'moblie': forms.NumberInput(attrs={'class': 'form-control'}), 
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),  # Adding password1 field with Bootstrap
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),  # Adding password2 field with Bootstrap
        }

class Booking_Form(forms.ModelForm) : 
    class Meta : 
        model = Booking
        fields = ['types' ,'check_in' , 'check_out' , 'time']

        widgets = {
                'types' : forms.Select(attrs={'class' : 'form-control'}) , 
                'check_in' : forms.DateInput(attrs={'class' : 'form-control' }),
                'check_out' : forms.DateInput(attrs={'class' : 'form-control' }) ,
                'time' : forms.TimeInput(attrs={'class' : 'form-control'})
                } 
                

    
