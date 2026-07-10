import pytest
from django.urls import reverse

pytestmark = pytest.mark.django_db


def test_home_renders_all_sections(client):
    response = client.get(reverse("website:home"))
    content = response.content.decode()
    assert response.status_code == 200
    for copy in [
        "Every Tail",
        "Happy Tale.",
        "Born From Love,",
        'Our <span class="text-gold">Services</span>',
        "Why Dogs Love",
        "Life at",
        "Ready to make your pup's day?",
        "Frequently Asked Questions",
        "Paw Paw Land. All rights reserved.",
    ]:
        assert copy in content, f"missing section copy: {copy}"


def test_home_shows_seeded_content(client, django_user_model):
    from django.core.management import call_command

    call_command("seed_demo")
    content = client.get(reverse("website:home")).content.decode()
    assert "Dog Daycare" in content
    assert "From $45/day" in content
    assert "Sarah Mitchell" in content
    assert "What does my dog need before their first visit?" in content


@pytest.mark.parametrize("name", ["about", "services", "gallery", "contact"])
def test_stub_pages_render(client, name):
    response = client.get(reverse(f"website:{name}"))
    assert response.status_code == 200
