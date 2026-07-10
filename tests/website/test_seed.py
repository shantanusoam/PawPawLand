import pytest
from django.core.management import call_command

from website.models import FAQ, GalleryImage, Service, Testimonial

pytestmark = pytest.mark.django_db


def test_seed_demo_is_idempotent():
    call_command("seed_demo")
    counts = (
        Service.objects.count(),
        Testimonial.objects.count(),
        FAQ.objects.count(),
        GalleryImage.objects.count(),
    )
    assert counts == (4, 3, 4, 11)
    call_command("seed_demo")
    assert Service.objects.count() == 4
    assert GalleryImage.objects.count() == 11


def test_seed_attaches_service_images():
    call_command("seed_demo")
    assert all(service.image for service in Service.objects.all())
