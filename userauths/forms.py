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
from .models import Profile, User
from django.forms import FileInput

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

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']

class ProfileUpdateForm(forms.ModelForm):
    
    class Meta:
        model = Profile
        fields = [
            'image',
            'full_name', 
            'phone',
            'gender',
            'country',
            'city',
            'state',
            'address',
            'identity_type',
            'identity_image',
            'facebook',
            'twitter',
        ]
        widgets = {
            'image': FileInput(attrs={'onchange': 'loadFile(event)', 'class':'upload'}),
        }


# forms.py

from django import forms
from hotel.models import Hotel
from taggit.forms import TagWidget
from django_ckeditor_5.widgets import CKEditor5Widget

class HotelForm(forms.ModelForm):
    """
    Form for creating and updating Hotel instances.
    """

    class Meta:
        model = Hotel
        # Include only the fields that should be editable by the user
        fields = [
            'name',
            'description',
            'image',
            'address',
            'mobile',
            'email',
            'status',
            'tags',
            'featured'
        ]
        widgets = {
            # Use CKEditor for the description field
            'description': CKEditor5Widget(config_name='extends'),
            # Use a select dropdown for status
            'status': forms.Select(attrs={'class': 'form-control'}),
            # Use TagWidget for tags to allow multiple tag selections
            'tags': TagWidget(attrs={'class': 'form-control'}),
            # Add CSS classes for better styling (optional)
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter hotel name'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter address'}),
            'mobile': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter mobile number'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email address'}),
            'featured': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'name': 'Hotel Name',
            'description': 'Description',
            'image': 'Hotel Image',
            'address': 'Address',
            'mobile': 'Mobile Number',
            'email': 'Email Address',
            'status': 'Status',
            'tags': 'Tags',
            'featured': 'Featured',
        }

    def clean_mobile(self):
        """
        Validate the mobile number to ensure it contains only digits and has a reasonable length.
        """
        mobile = self.cleaned_data.get('mobile')
        if not mobile.isdigit():
            raise forms.ValidationError("Mobile number must contain only digits.")
        if len(mobile) < 10:
            raise forms.ValidationError("Mobile number must be at least 10 digits.")
        return mobile

    def clean_email(self):
        """
        Ensure that the email address is valid. This is somewhat redundant since EmailField already does this,
        but it's here for demonstration or additional validation if needed.
        """
        email = self.cleaned_data.get('email')
        if email:
            try:
                forms.EmailField().clean(email)
            except forms.ValidationError:
                raise forms.ValidationError("Enter a valid email address.")
        return email

    def clean_image(self):
        """
        Optionally, add validation for the uploaded image.
        For example, check file size or type.
        """
        image = self.cleaned_data.get('image')
        if image:
            if image.size > 5 * 1024 * 1024:  # Limit to 5MB
                raise forms.ValidationError("Image file too large ( > 5MB ).")
            if not image.content_type in ['image/jpeg', 'image/png', 'image/jpg']:
                raise forms.ValidationError("Unsupported file type. Only JPEG and PNG are allowed.")
        return image
    
    
