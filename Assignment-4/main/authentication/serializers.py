from rest_framework import serializers
from .models import UserProfile
import re


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'name', 'age', 'website', 'email', 'phone_number']

    def validate_name(self, value):
        if re.search(r"[;'\"--]", value):
            raise serializers.ValidationError("Invalid characters in name.")
        return value

    def validate_age(self, value):
        if value < 18 or value > 120:
            raise serializers.ValidationError("Age must be between 18 and 120.")
        return value

    def validate_website(self, value):
        if not value.startswith('http://') and not value.startswith('https://'):
            raise serializers.ValidationError("Website must start with 'http://' or 'https://'.")
        return value
