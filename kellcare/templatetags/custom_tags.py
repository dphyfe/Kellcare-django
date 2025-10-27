from django import template
from datetime import datetime
import random

register = template.Library()


@register.simple_tag
def current_time():
    """Returns the current time"""
    return datetime.now().strftime("%B %d, %Y at %I:%M %p")


@register.simple_tag
def random_quote():
    """Returns a random healthcare quote"""
    quotes = [
        "Your health is your wealth.",
        "Prevention is better than cure.",
        "Caring for your body is the first step to caring for your mind.",
        "Health is not just about what you're eating. It's also about what you're thinking and saying.",
        "Take care of your body. It's the only place you have to live.",
    ]
    return random.choice(quotes)


@register.simple_tag
def calculate_age(year_founded):
    """Calculate how many years since founding"""
    return datetime.now().year - year_founded


@register.inclusion_tag("kellcare/includes/custom_widget.html")
def custom_info_widget(title, value, icon=""):
    """Renders a custom info widget"""
    return {"title": title, "value": value, "icon": icon}


@register.filter
def multiply(value, arg):
    """Multiply the value by the argument"""
    try:
        return int(value) * int(arg)
    except (ValueError, TypeError):
        return 0


@register.filter
def format_phone(phone_number):
    """Format phone number"""
    # Remove non-digits
    digits = "".join(filter(str.isdigit, str(phone_number)))
    if len(digits) == 10:
        return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
    return phone_number


@register.simple_tag
def format_address(address_dict):
    """Format a complete address from dictionary"""
    if not address_dict:
        return ""

    parts = []
    if address_dict.get("street"):
        parts.append(address_dict["street"])
    if address_dict.get("district"):
        parts.append(address_dict["district"])

    city_state_zip = []
    if address_dict.get("city"):
        city_state_zip.append(address_dict["city"])
    if address_dict.get("state"):
        city_state_zip.append(address_dict["state"])
    if address_dict.get("zip"):
        city_state_zip.append(address_dict["zip"])

    if city_state_zip:
        parts.append(", ".join(city_state_zip))

    return "<br>".join(parts)


@register.simple_tag
def phone_link(phone_number):
    """Generate a tel: link from phone number"""
    digits = "".join(filter(str.isdigit, str(phone_number)))
    return f"tel:+1{digits}" if len(digits) == 10 else f"tel:{digits}"
