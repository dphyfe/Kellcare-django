from datetime import datetime


def global_context(request):
    """
    Context processor to add site-wide context variables
    These will be available in ALL templates
    """
    return {
        "site_name": "Kellcare Healthcare",
        "current_year": datetime.now().year,
        "support_phone": "1-800-KELLCARE",
        "support_email": "support@kellcare.com",
        "social_media": {
            "facebook": "https://facebook.com/kellcare",
            "twitter": "https://twitter.com/kellcare",
            "linkedin": "https://linkedin.com/company/kellcare",
        },
        "business_hours": {
            "weekdays": "8:00 AM - 8:00 PM",
            "weekends": "9:00 AM - 5:00 PM",
            "emergency": "24/7",
        },
        "quick_stats": {
            "patients_served": "2M+",
            "years_experience": datetime.now().year - 1995,
            "satisfaction_rate": "98.5%",
        },
    }
