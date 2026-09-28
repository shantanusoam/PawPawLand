import pytest
from django.urls import reverse

from website.models import Registration

pytestmark = pytest.mark.django_db


def test_registration_page_renders_form(client):
    response = client.get(reverse("website:registration"))
    content = response.content.decode()
    assert response.status_code == 200
    assert "Full Name" in content
    assert "Dog&#x27;s Name" in content
    assert "food allergies" in content


def test_registration_form_valid_submission_saves_and_redirects(client):
    response = client.post(
        reverse("website:registration"),
        {
            "full_name": "Jamie Smith",
            "email": "jamie@example.com",
            "phone": "0400 000 000",
            "dog_name": "Biscuit",
            "food_allergies": "No chicken, please.",
            "instagram_handle": "@biscuit_the_dog",
        },
    )
    assert response.status_code == 302
    assert Registration.objects.count() == 1
    registration = Registration.objects.get()
    assert registration.dog_name == "Biscuit"
    assert registration.full_name == "Jamie Smith"
    assert registration.instagram_handle == "@biscuit_the_dog"
    assert registration.is_read is False


def test_registration_form_missing_required_fields_does_not_save(client):
    response = client.post(
        reverse("website:registration"), {"full_name": "", "email": "", "dog_name": ""}
    )
    assert response.status_code == 200
    assert Registration.objects.count() == 0


def test_registration_form_optional_fields_can_be_left_blank(client):
    response = client.post(
        reverse("website:registration"),
        {
            "full_name": "Jamie Smith",
            "email": "jamie@example.com",
            "dog_name": "Biscuit",
        },
    )
    assert response.status_code == 302
    assert Registration.objects.count() == 1
