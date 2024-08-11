from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Appointment

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']

class AppointmentForm(forms.ModelForm):
    appointment_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    appointment_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))

    class Meta:
        model = Appointment
        fields = ['doctor_name', 'appointment_date', 'appointment_time', 'description', 'symptoms', 'patient_details']
        widgets = {
            'appointment_date': forms.DateInput(attrs={'type': 'date'}),  # Using DateInput for just the date
            'appointment_time': forms.TimeInput(attrs={'type': 'time'}),  # Adding the appointment time widget
            'description': forms.Textarea(attrs={'rows': 4}),  # Optional: Improve textarea appearance
            'symptoms': forms.Textarea(attrs={'rows': 4}),  # Optional: Improve textarea appearance
            'patient_details': forms.Textarea(attrs={'rows': 4}),  # Optional: Improve textarea appearance
        }
