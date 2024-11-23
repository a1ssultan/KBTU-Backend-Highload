from django import forms
from .models import UserProfile
import re


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['name', 'age', 'website', 'email']

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if re.search(r"[;'\"--]", name):
            raise forms.ValidationError("Invalid characters in name.")
        return name

    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age < 18 or age > 120:
            raise forms.ValidationError("Age must be between 18 and 120.")
        return age

    def clean_website(self):
        website = self.cleaned_data.get('website')
        if not website.startswith('http://') and not website.startswith('https://'):
            raise forms.ValidationError("Website must start with 'http://' or 'https://'.")
        return website

    def clean_email(self):
        email = self.cleaned_data.get('email')
        return email
