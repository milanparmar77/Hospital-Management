from django.db import models
from patient.models import Patient
from doctor.models import Doctor

STATUS_CHOICES = [
    ('Pending', 'Pending'),
    ('Approved', 'Approved'),
    ('Completed', 'Completed'),
    ('Cancelled', 'Cancelled'),
]

class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES , default='Pending')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['doctor', 'date', 'time'],
                name='unique_appointment'
            )
        ]

    def __str__(self):
        return f"{self.doctor} - {self.date} - {self.time}"
    
    