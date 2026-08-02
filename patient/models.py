from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

phone_validator = RegexValidator(
    regex=r'^[6-9]\d{9}$',
    message="Enter valid Indian phone number (10 digits starting from 6-9)"
)

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.PositiveIntegerField(null=True, blank=True)
    # def clean(self):
    
        # if self.age < 0 or self.age > 120:
        #     raise ValidationError("Age must be between 0 and 120")
        
    gender = models.CharField(max_length=10)
    phone = models.CharField(max_length=15, validators=[phone_validator])

    def __str__(self):
        return self.user.username