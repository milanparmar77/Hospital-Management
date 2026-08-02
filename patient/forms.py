from django import forms
from django.core.validators import RegexValidator

phone_validator = RegexValidator(
    regex=r"^\+?[0-9\s\-]{7,15}$",
    message="Enter a valid phone number (digits, spaces, dashes, optional leading +).",
)


class EditProfileForm(forms.Form):
   
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    email = forms.EmailField()
    phone = forms.CharField(max_length=20, validators=[phone_validator])
    profile_image = forms.ImageField(required=False)