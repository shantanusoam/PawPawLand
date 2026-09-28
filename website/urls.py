from django.urls import path
from django.views.generic.base import RedirectView

from . import views

app_name = "website"

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("services/", views.services, name="services"),
    # Old slug from before the Puppy Playground → Puppy Playgroup rename.
    path(
        "services/puppy-playground/",
        RedirectView.as_view(pattern_name="website:service_detail", permanent=True),
        {"slug": "puppy-playgroup"},
    ),
    path("services/<slug:slug>/", views.service_detail, name="service_detail"),
    path("gallery/", views.gallery, name="gallery"),
    path("contact/", views.contact, name="contact"),
]
