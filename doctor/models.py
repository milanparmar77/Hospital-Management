from django.db import models
from django.contrib.auth.models import User

class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    qualifications = models.CharField(max_length=150, default="MBBS")
    experience = models.PositiveIntegerField(help_text="Experience in years", default=0)
    department = models.CharField(max_length=100, default="General Medicine")
    consultation_fee = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    available_days = models.CharField(max_length=100, default="Monday-Friday")
    available_time = models.CharField(max_length=100, default="09:00 AM - 05:00 PM")

    def __str__(self):
        return f"Dr. {self.user.first_name} {self.user.last_name}"

