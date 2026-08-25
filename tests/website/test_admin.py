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
    for label in [
        "Services",
        "Testimonials",
        "FAQs",
        "Gallery images",
        "Pricing plans",
        "Team members",
        "Site settings",
        "Contact submissions",
    ]:
        assert label in content


def test_service_add_form_uses_tinymce(admin_client_logged_in):
    content = admin_client_logged_in.get(reverse("admin:website_service_add")).content.decode()
    assert "tinymce" in content.lower()


def test_team_member_add_form_uses_tinymce(admin_client_logged_in):
    content = admin_client_logged_in.get(reverse("admin:website_teammember_add")).content.decode()
    assert "tinymce" in content.lower()


def test_site_settings_is_singleton_in_admin(admin_client_logged_in):
    from website.models import SiteSettings

    # Visiting the changelist redirects straight to the one editable row.
    response = admin_client_logged_in.get(reverse("admin:website_sitesettings_changelist"))
    assert response.status_code == 302
    assert SiteSettings.objects.count() == 1

    add_response = admin_client_logged_in.get(reverse("admin:website_sitesettings_add"))
    assert add_response.status_code == 403


def test_contact_submissions_are_visible_but_not_addable(admin_client_logged_in):
    from website.models import ContactSubmission

    ContactSubmission.objects.create(
        full_name="Jamie Smith", email="jamie@example.com", message="Hi there"
    )
    content = admin_client_logged_in.get(
        reverse("admin:website_contactsubmission_changelist")
    ).content.decode()
    assert "Jamie Smith" in content

    add_response = admin_client_logged_in.get(reverse("admin:website_contactsubmission_add"))
    assert add_response.status_code == 403
