import pytest
from django.urls import reverse

from website.models import Registration

pytestmark = pytest.mark.django_db

VALID_PAYLOAD = {
    "owner_name": "Jamie Smith",
    "address": "123 Example Street",
    "suburb": "Blackburn",
    "postcode": "3130",
    "phone": "0400 000 000",
    "email": "jamie@example.com",
    "emergency_contact_name": "Alex Smith",
    "emergency_contact_phone": "0400 111 222",
    "vet_clinic_name": "Blackburn Vet Clinic",
    "vet_phone": "0400 333 444",
    "dog_name": "Biscuit",
    "microchip_number": "123456789012345",
    "breed": "Golden Retriever",
    "colour": "Golden",
    "date_of_birth": "2022-01-15",
    "gender": "male",
    "is_desexed": "yes",
    "has_aggression": "no",
    "last_vaccination_date": "2026-01-01",
    "has_health_ailments": "no",
    "has_medication": "no",
    "agreed_to_terms": "on",
}


def test_registration_page_renders_form(client):
    response = client.get(reverse("website:registration"))
    content = response.content.decode()
    assert response.status_code == 200
    for copy in [
        "Owner&#x27;s Name",
        "Emergency Contact Details",
        "Vet's Details",
        "Name of Dog",
        "Microchip Number",
        "Desexed?",
        "Aggression to dogs or people?",
        "Last Vaccination Date",
        "Health ailments?",
        "Medication?",
        "food allergies",
        "Instagram Stories",
        "I agree with the Terms &amp; Conditions",
    ]:
        assert copy in content, f"missing: {copy}"


def test_registration_form_valid_submission_saves_and_redirects(client):
    response = client.post(reverse("website:registration"), VALID_PAYLOAD)
    assert response.status_code == 302
    assert Registration.objects.count() == 1
    registration = Registration.objects.get()
    assert registration.dog_name == "Biscuit"
    assert registration.owner_name == "Jamie Smith"
    assert registration.agreed_to_terms is True
    assert registration.is_read is False


def test_registration_form_submission_emails_site_settings_address(client, mailoutbox):
    from website.models import SiteSettings

    settings_obj = SiteSettings.load()
    settings_obj.email = "info@pawpawland.au"
    settings_obj.save()

    client.post(reverse("website:registration"), VALID_PAYLOAD)
    assert len(mailoutbox) == 1
    assert mailoutbox[0].to == ["info@pawpawland.au"]
    assert "Biscuit" in mailoutbox[0].subject
    assert "Jamie Smith" in mailoutbox[0].subject
    assert "Golden Retriever" in mailoutbox[0].body


def test_registration_form_missing_required_fields_does_not_save(client):
    response = client.post(reverse("website:registration"), {})
    assert response.status_code == 200
    assert Registration.objects.count() == 0


def test_registration_form_requires_agreeing_to_terms(client):
    payload = {**VALID_PAYLOAD}
    del payload["agreed_to_terms"]
    response = client.post(reverse("website:registration"), payload)
    assert response.status_code == 200
    assert Registration.objects.count() == 0


def test_registration_form_optional_fields_can_be_left_blank(client):
    response = client.post(reverse("website:registration"), VALID_PAYLOAD)
    assert response.status_code == 302
    registration = Registration.objects.get()
    assert registration.food_allergies == ""
    assert registration.instagram_handle == ""
    assert not registration.dog_photo
    assert not registration.vaccination_certificate


def test_registration_form_saves_optional_extras_when_provided(client):
    payload = {
        **VALID_PAYLOAD,
        "food_allergies": "No chicken, please.",
        "instagram_handle": "@biscuit_the_dog",
    }
    response = client.post(reverse("website:registration"), payload)
    assert response.status_code == 302
    registration = Registration.objects.get()
    assert registration.food_allergies == "No chicken, please."
    assert registration.instagram_handle == "@biscuit_the_dog"
