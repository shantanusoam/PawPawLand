from .models import Service, SiteSettings


def site_globals(request):
    """Data needed on every page: the header's Services dropdown and site-wide contact info."""
    return {
        "nav_services": Service.objects.filter(is_active=True),
        "site_settings": SiteSettings.load(),
    }
