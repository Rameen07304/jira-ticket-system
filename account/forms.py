

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .models import CustomUser, CITY_CHOICES, COUNTRY_CHOICES
from django.core.exceptions import ValidationError
import re

    
def validate_password(value):
    if len(value) < 8:
        raise ValidationError("Password must be at least 8 characters long")
    if not re.search(r'[A-Z]', value):
        raise ValidationError("Password must contain at least one uppercase letter")
    if not re.search(r'[a-z]', value):
        raise ValidationError("Password must contain at least one lowercase letter")
    if not re.search(r'[0-9]', value):
        raise ValidationError("Password must contain at least one digit")
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
        raise ValidationError("Password must contain at least one special character")
    
COUNTRY_CITY_MAP = {
    'PK': ['KHI', 'LHR', 'ISB'],
    'IN': ['DEL'],
    'US': ['NYC'],
    'UK': ['LON'],
    'JP': ['TKY'],
    'AU': ['SYD'],
}
    
class RegisterForm(forms.ModelForm):
    #User fields
    username= forms.CharField(max_length=150)  
    password = forms.CharField(widget=forms.PasswordInput, validators=[validate_password])
    email= forms.EmailField()
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    
    #Custom user fields
    dob = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}),required=False, help_text="Optional")
    city = forms.ChoiceField(choices=CITY_CHOICES,required=False, help_text="Optional")
    country = forms.ChoiceField(choices=COUNTRY_CHOICES,required=False, help_text="Optional")
    pincode = forms.CharField(max_length=10, required=False, help_text="Optional")
    address = forms.CharField(widget=forms.Textarea, required=False, help_text="Optional")

    class Meta:
        model = User
        fields = ['username', 'email', 'password','first_name','last_name','dob']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email is already registered.")
        return email
    
    def clean(self):
        cleaned_data = super().clean()
        city = cleaned_data.get('city')
        country = cleaned_data.get('country')

        if country and city:
            if city not in COUNTRY_CITY_MAP.get(country, []):
                self.add_error('city', f"Invalid city '{city}' for the selected country '{country}'.")

        return cleaned_data


class LoginForm(AuthenticationForm):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
