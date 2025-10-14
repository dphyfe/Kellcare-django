from django import forms
from .models import ContactMessage, Appointment


class ContactForm(forms.ModelForm):
    """Form for contact page"""

    class Meta:
        model = ContactMessage
        fields = ["name", "email", "phone", "subject", "message"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Your full name"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "your.email@example.com"}),
            "phone": forms.TextInput(attrs={"class": "form-control", "placeholder": "+1 (555) 123-4567"}),
            "subject": forms.TextInput(attrs={"class": "form-control", "placeholder": "Subject of your message"}),
            "message": forms.Textarea(attrs={"class": "form-control", "rows": 5, "placeholder": "Your message here..."}),
        }


class AppointmentForm(forms.ModelForm):
    """Form for booking appointments"""

    class Meta:
        model = Appointment
        fields = ["doctor", "appointment_date", "reason"]
        widgets = {
            "doctor": forms.Select(attrs={"class": "form-control"}),
            "appointment_date": forms.DateTimeInput(attrs={"class": "form-control", "type": "datetime-local"}),
            "reason": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Please describe the reason for your visit..."}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only show available doctors
        from .models import Doctor

        self.fields["doctor"].queryset = Doctor.objects.filter(is_available=True)
