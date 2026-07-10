import pytest
from django.urls import reverse

pytestmark = pytest.mark.django_db


@pytest.fixture
def admin_client_logged_in(client, django_user_model):
    django_user_model.objects.create_superuser("admin", "admin@example.com", "password")
    client.login(username="admin", password="password")
    return client


def test_admin_index_lists_content_models(admin_client_logged_in):
    content = admin_client_logged_in.get(reverse("admin:index")).content.decode()
    for label in ["Services", "Testimonials", "FAQs", "Gallery images"]:
        assert label in content


def test_service_add_form_uses_tinymce(admin_client_logged_in):
    content = admin_client_logged_in.get(reverse("admin:website_service_add")).content.decode()
    assert "tinymce" in content.lower()
