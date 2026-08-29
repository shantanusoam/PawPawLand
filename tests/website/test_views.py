import pytest
from django.urls import reverse

pytestmark = pytest.mark.django_db


def test_home_renders_all_sections(client):
    response = client.get(reverse("website:home"))
    content = response.content.decode()
    assert response.status_code == 200
    for copy in [
        "Every Tail",
        "ppy Tale.",
        "tail-wagging adventures",
        "hero-dog-wrap",
        "Born From Love,",
        "What We Offer",
        "Why Dogs Love",
        "Life at",
        "Ready to make your pup's day?",
        "Frequently Asked Questions",
        "Paw Paw Land. All rights reserved.",
    ]:
        assert copy in content, f"missing section copy: {copy}"


def test_home_hero_dog_overlaps_wave(client):
    content = client.get(reverse("website:home")).content.decode()
    assert "hero-dog-wrap" in content
    assert "lg:-mb-28" in content
    assert 'id="hero-dog"' in content


def test_home_hero_heading_uses_navy_not_faded_line(client):
    content = client.get(reverse("website:home")).content.decode()
    assert "text-navy/45" not in content
    assert "From playful days to cozy nights" in content

    from django.core.management import call_command

    call_command("seed_demo")
    content = client.get(reverse("website:home")).content.decode()
    assert "Dog Daycare" in content
    assert "From $45/day" in content
    assert "Sarah Mitchell" in content
    assert "What does my dog need before their first visit?" in content


def test_gallery_page_renders(client):
    response = client.get(reverse("website:gallery"))
    assert response.status_code == 200


def test_about_page_renders_team_and_shared_sections(client):
    from django.core.management import call_command

    call_command("seed_demo")
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
    # Each team member shows their own bio, not a shared/duplicated one.
    assert content.count("Crocosaurus Cove") == 1
    assert content.count("Labrador named Sage") == 1


def test_services_page_renders_pricing_plans(client):
    from django.core.management import call_command

    call_command("seed_demo")
    response = client.get(reverse("website:services"))
    content = response.content.decode()
    assert response.status_code == 200
    for copy in [
        "Needs &amp; Loves",
        "Give Your Pup More Play &amp;",
        "Two Pups,",
        "Dog Daycare",
        "Dog Grooming",
        "Puppy Playground",
        "Dog Birthday Parties",
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


def test_services_hub_page_is_distinct_from_daycare_detail_page(client):
    from django.core.management import call_command

    call_command("seed_demo")
    hub_content = client.get(reverse("website:services")).content.decode()
    daycare_content = client.get(
        reverse("website:service_detail", args=["dog-daycare"])
    ).content.decode()
    # The hub page must not just be reusing the Daycare page's hero/intro copy.
    # ("Meet & Greet" is baked into heading-daycare.svg, not live text, so only the
    # intro heading — real text on both pages before this fix — is checked here.)
    assert "A Happy Day," not in hub_content
    assert "A Happy Day," in daycare_content
    assert "Needs &amp; Loves" in hub_content
    assert "Needs &amp; Loves" not in daycare_content


def test_services_page_shows_services_grid_first(client):
    from django.core.management import call_command

    call_command("seed_demo")
    content = client.get(reverse("website:services")).content.decode()
    # "Our Services" grid renders right after the hero, before pricing and the CTA.
    assert content.index("What We Offer") < content.index("Two Pups,")
    assert content.index("Two Pups,") < content.index("Ready to make your pup's day?")


def test_header_dropdown_links_to_service_detail_pages(client):
    from django.core.management import call_command

    call_command("seed_demo")
    home = client.get(reverse("website:home")).content.decode()
    for slug in ["dog-daycare", "dog-grooming", "puppy-playground", "dog-birthday-parties"]:
        assert f'href="/services/{slug}/"' in home


@pytest.mark.parametrize(
    ("slug", "expected_heading"),
    [
        ("dog-daycare", "First 3 sessions for $75"),
        ("puppy-playground", "A Little Adventure"),
        ("dog-birthday-parties", "A Party"),
        ("dog-grooming", "A Fresh"),
    ],
)
def test_service_detail_pages_render_unique_content(client, slug, expected_heading):
    from django.core.management import call_command

    call_command("seed_demo")
    response = client.get(reverse("website:service_detail", args=[slug]))
    content = response.content.decode()
    assert response.status_code == 200
    assert expected_heading in content
    # Universal pricing plans still appear on every service detail page.
    assert "Casual Day" in content
    assert "Double Paw Day" in content


def test_service_detail_404s_for_unknown_slug(client):
    response = client.get("/services/not-a-real-service/")
    assert response.status_code == 404


def test_gallery_page_shows_seeded_images(client):
    from django.core.management import call_command

    call_command("seed_demo")
    response = client.get(reverse("website:gallery"))
    content = response.content.decode()
    assert response.status_code == 200
    assert content.count("<img") >= 11


def test_footer_uses_site_settings(client):
    from django.core.management import call_command

    call_command("seed_demo")
    content = client.get(reverse("website:home")).content.decode()
    assert "(02) 9123 4567" in content
    assert "hello@pawpawland.com.au" in content
    assert "123 Happy Paws Lane, Sydney NSW 2000" in content
