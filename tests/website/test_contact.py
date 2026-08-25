import pytest
from django.urls import reverse

from website.models import ContactSubmission

pytestmark = pytest.mark.django_db


def test_contact_page_renders_form(client):
    response = client.get(reverse("website:contact"))
    content = response.content.decode()
    assert response.status_code == 200
    assert "Full Name" in content
    assert "Enquiry" in content


def test_contact_form_valid_submission_saves_and_redirects(client):
    response = client.post(
        reverse("website:contact"),
        {
            "full_name": "Jamie Smith",
            "email": "jamie@example.com",
            "phone": "0400 000 000",
            "service_requested": "Dog Daycare",
            "message": "Do you have space this weekend?",
        },
    )
    assert response.status_code == 302
    assert ContactSubmission.objects.count() == 1
    submission = ContactSubmission.objects.get()
    assert submission.full_name == "Jamie Smith"
    assert submission.email == "jamie@example.com"
    assert submission.is_read is False


def test_contact_form_missing_required_fields_does_not_save(client):
    response = client.post(reverse("website:contact"), {"full_name": "", "email": ""})
    assert response.status_code == 200
    assert ContactSubmission.objects.count() == 0


def test_contact_form_invalid_email_does_not_save(client):
    response = client.post(
        reverse("website:contact"),
        {"full_name": "Jamie Smith", "email": "not-an-email", "message": "Hi"},
    )
    assert response.status_code == 200
    assert ContactSubmission.objects.count() == 0
