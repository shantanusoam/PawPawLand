import pytest
from django.urls import reverse

pytestmark = pytest.mark.django_db


def test_home_renders_all_sections(client):
    response = client.get(reverse("website:home"))
    content = response.content.decode()
    assert response.status_code == 200
    for copy in [
        "home away from home",
        "for your dog",
        "furry friendship",
        "hero-dog-wrap",
        "Happy Dogs",
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
    assert "Where days are filled with play" in content

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
        "Puppy Playgroup",
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


def test_pricing_card_shows_split_layout_only_when_price_2_is_set(client):
    from website.models import PricingPlan

    PricingPlan.objects.create(
        name="Casual Day",
        dog_count=1,
        price="46.00",
        period_label="Half-Day",
        price_caption="Ideal for shorter visits",
        price_2="65.00",
        period_label_2="Session",
        price_2_caption="Perfect for occasional daycare visits",
        features_text="Flexible drop-in care",
    )
    PricingPlan.objects.create(
        name="Value Pack",
        dog_count=1,
        price="305.00",
        period_label="10 Days",
        features_text="Ideal for regular daycare visits",
    )
    content = client.get(reverse("website:services")).content.decode()
    # Dual-price plan shows both prices and their captions.
    assert "$46" in content
    assert "Half-Day" in content
    assert "Ideal for shorter visits" in content
    assert "$65" in content
    assert "Session" in content
    assert "Perfect for occasional daycare visits" in content
    # Single-price plan is unaffected — no stray "/ None" or similar leaking through.
    assert "$305" in content
    assert "/ 10 Days" in content


def test_pricing_card_shows_three_way_split_when_price_3_is_set(client):
    from django.core.management import call_command

    from website.models import PricingPlan, Service

    call_command("seed_demo")
    PricingPlan.objects.create(
        name="Weekly Pass",
        service=Service.objects.get(slug="dog-daycare"),
        dog_count=1,
        price="46.00",
        period_label="Half-Day",
        price_2="65.00",
        period_label_2="Session",
        price_3="250.00",
        period_label_3="Full Week",
        price_3_caption="Best value for regulars",
        features_text="Flexible drop-in care",
    )
    content = client.get(reverse("website:service_detail", args=["dog-daycare"])).content.decode()
    assert "$250" in content
    assert "Full Week" in content
    assert "Best value for regulars" in content


def test_service_detail_page_shows_gallery_only_for_tagged_photos(client):
    from django.core.files.uploadedfile import SimpleUploadedFile
    from django.core.management import call_command

    from website.models import GalleryImage, Service

    call_command("seed_demo")
    GalleryImage.objects.create(
        alt_text="Puppy at the water bowl",
        service=Service.objects.get(slug="dog-grooming"),
        row=1,
        image=SimpleUploadedFile("puppy.jpg", b"fake-image-bytes", content_type="image/jpeg"),
    )
    grooming_content = client.get(
        reverse("website:service_detail", args=["dog-grooming"])
    ).content.decode()
    puppy_content = client.get(
        reverse("website:service_detail", args=["puppy-playgroup"])
    ).content.decode()
    assert "Puppy at the water bowl" in grooming_content
    assert "Puppy at the water bowl" not in puppy_content


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


def test_services_hub_page_shows_gallery_between_pricing_and_cta(client):
    from django.core.management import call_command

    call_command("seed_demo")
    content = client.get(reverse("website:services")).content.decode()
    assert content.index("Two Pups,") < content.index("Life at")
    assert content.index("Life at") < content.index("Ready to make your pup's day?")


def test_header_dropdown_links_to_service_detail_pages(client):
    from django.core.management import call_command

    call_command("seed_demo")
    home = client.get(reverse("website:home")).content.decode()
    for slug in ["dog-daycare", "dog-grooming", "puppy-playgroup", "dog-birthday-parties"]:
        assert f'href="/services/{slug}/"' in home


@pytest.mark.parametrize(
    ("slug", "expected_heading"),
    [
        ("dog-daycare", "First 3 sessions for $75"),
        ("puppy-playgroup", "Little Paws."),
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


def test_service_pricing_plans_are_scoped_to_their_own_service(client):
    from django.core.management import call_command

    call_command("seed_demo")
    daycare_content = client.get(
        reverse("website:service_detail", args=["dog-daycare"])
    ).content.decode()
    grooming_content = client.get(
        reverse("website:service_detail", args=["dog-grooming"])
    ).content.decode()
    # Seeded plans belong to Daycare only — they must not leak onto other services.
    assert "Casual Day" in daycare_content
    assert "Double Paw Day" in daycare_content
    assert "Casual Day" not in grooming_content
    assert "Double Paw Day" not in grooming_content


def test_service_detail_404s_for_unknown_slug(client):
    response = client.get("/services/not-a-real-service/")
    assert response.status_code == 404


def test_old_puppy_playground_slug_redirects_to_puppy_playgroup(client):
    response = client.get("/services/puppy-playground/")
    assert response.status_code == 301
    assert response.url == "/services/puppy-playgroup/"


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
