from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


class Appointment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    doctor_name = models.CharField(max_length=100)
    appointment_date = models.DateTimeField()
    description = models.TextField()
    symptoms = models.TextField()  # Add this line
    patient_details = models.TextField(default="N/A")  # Add this line

    def __str__(self):
        return f"{self.doctor_name} - {self.appointment_date}"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.user.username
