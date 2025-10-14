from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ContactForm


def home(request):
    """Home page view"""
    return render(request, "kellcare/home.html")


def about(request):
    """About page view"""
    return render(request, "kellcare/about.html")


def services(request):
    """Services page view"""
    return render(request, "kellcare/services.html")


# advanced function with defaults
def contact(request, customer_name=None, customer_email=None):
    """Contact page view"""
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thank you for your message! We will get back to you soon.")
            return redirect("kellcare:contact")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ContactForm()

    return render(request, "kellcare/contact.html", {"form": form})
