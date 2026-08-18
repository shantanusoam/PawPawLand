import pytest
from django.core.management import call_command

from website.models import (
    FAQ,
    GalleryImage,
    PricingPlan,
    Service,
    SiteSettings,
    TeamMember,
    Testimonial,
)

pytestmark = pytest.mark.django_db


def test_seed_demo_is_idempotent():
    call_command("seed_demo")
    counts = (
        Service.objects.count(),
        Testimonial.objects.count(),
        FAQ.objects.count(),
        GalleryImage.objects.count(),
        PricingPlan.objects.count(),
        TeamMember.objects.count(),
        SiteSettings.objects.count(),
    )
    assert counts == (4, 3, 4, 11, 6, 2, 1)
    call_command("seed_demo")
    assert Service.objects.count() == 4
    assert GalleryImage.objects.count() == 11
    assert PricingPlan.objects.count() == 6
    assert TeamMember.objects.count() == 2
    assert SiteSettings.objects.count() == 1


def test_seed_attaches_service_images():
    call_command("seed_demo")
    assert all(service.image for service in Service.objects.all())
    assert all(plan.photo for plan in PricingPlan.objects.all())
    assert all(member.photo for member in TeamMember.objects.all())


def test_seed_pricing_plans_split_by_dog_count():
    call_command("seed_demo")
    assert PricingPlan.objects.filter(dog_count=1).count() == 3
    assert PricingPlan.objects.filter(dog_count=2).count() == 3


def test_seed_site_settings_populated():
    call_command("seed_demo")
    settings_obj = SiteSettings.load()
    assert settings_obj.phone == "(02) 9123 4567"
    assert settings_obj.email == "hello@pawpawland.com.au"
