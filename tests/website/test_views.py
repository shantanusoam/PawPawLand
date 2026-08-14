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
        "What We Offer",
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


@pytest.mark.parametrize("name", ["gallery", "contact"])
def test_stub_pages_render(client, name):
    response = client.get(reverse(f"website:{name}"))
    assert response.status_code == 200


def test_about_page_renders_team_and_shared_sections(client):
    response = client.get(reverse("website:about"))
    content = response.content.decode()
    assert response.status_code == 200
    for copy in [
        "Meet the humans behind the",
        "happy tails.",
        "Born From Love,",
        "The pack",
        "behind the pack.",
        "Karen",
        "Leah",
        "Puppy Specialist",
        "Why Dogs Love",
        "Life at",
    ]:
        assert copy in content, f"missing section copy: {copy}"
    # Card 4 (Leah, second instance) must show Leah's own bio, not Karen's.
    assert content.count("Crocosaurus Cove") == 2
    assert content.count("Labrador named Sage") == 2


def test_services_page_renders_pricing_plans(client):
    response = client.get(reverse("website:services"))
    content = response.content.decode()
    assert response.status_code == 200
    for copy in [
        "Meet &amp; Greet",
        "A Happy Day,",
        "Give Your Pup More Play &amp;",
        "Two Pups,",
        "Casual Day",
        "$65",
        "Value Pack",
        "$305",
        "Paw-some Plan",
        "$1,100",
        "Double Paw Day",
        "$110",
        "Paws &amp; Play Pack",
        "$1,000",
        "Ultimate Paw Pack",
        "$1,900",
        "Ready to make your pup's day?",
    ]:
        assert copy in content, f"missing section copy: {copy}"
