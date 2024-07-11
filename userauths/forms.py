# from django import forms 
# from django.contrib.auth.forms import UserCreationForm
# from django.core.exceptions import ValidationError
# from .models import User

# from userauths.models import User, profile

# class UserRegisterForm(UserCreationForm):
#     full_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "Enter Full Name"}), max_length=100, required=True)

#     username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "Enter Preferred Username"}), max_length=100, required=True)

#     email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': "Email Adress"}), required=True)

#     phone = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "Phone Number"}), required=True)

#     password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': "Password"}), required=True)

#     password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': "Confirm Password"}), required=True)
 

#     # password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': "Your Password Must Match"}), required=True)
#     class Meta:
#         model = User
#         fields = ['full_name', 'username', 'phone', 'email', 'password1', 'password2']
#     def clean(self):
#         cleaned_data = super().clean()
#         password1 = cleaned_data.get("password1")
#         password2 = cleaned_data.get("password2")

#         if password1 and password2 and password1 != password2:
#             raise ValidationError("Passwords do not match")
        
#         return cleaned_data    



from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import User

class UserRegisterForm(UserCreationForm):
    full_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "Enter Full Name"}), max_length=100, required=True)
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "Enter Preferred Username"}), max_length=100, required=True)
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': "Email Address"}), required=True)
    phone = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "Phone Number"}), required=True)
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': "Password"}), required=True)
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': "Confirm Password"}), required=True)

    class Meta:
        model = User
        fields = ['full_name', 'username', 'phone', 'email', 'password1', 'password2']

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords do not match")
        
        return cleaned_data

