import pytest

from website.models import FAQ, PricingPlan, Service, SiteSettings, TeamMember, Testimonial

pytestmark = pytest.mark.django_db


def test_str_representations():
    service = Service.objects.create(
        name="Dog Daycare",
        slug="dog-daycare",
        emoji_badge="☀️",
        description="<p>Play all day.</p>",
        price_label="From $45/day",
    )
    testimonial = Testimonial.objects.create(
        author_name="Sarah Mitchell", dog_name="Biscuit the Golden", quote="<p>Great!</p>"
    )
    faq = FAQ.objects.create(question="When are you open?", answer="<p>Every day.</p>")
    assert str(service) == "Dog Daycare"
    assert str(testimonial) == "Sarah Mitchell (Biscuit the Golden)"
    assert str(faq) == "When are you open?"


def test_ordering_by_sort_order():
    FAQ.objects.create(question="Second", answer="<p>b</p>", sort_order=2)
    FAQ.objects.create(question="First", answer="<p>a</p>", sort_order=1)
    assert [faq.question for faq in FAQ.objects.all()] == ["First", "Second"]


def test_pricing_plan_feature_list_and_price_display():
    plan = PricingPlan.objects.create(
        name="Casual Day",
        dog_count=1,
        price="1100.00",
        period_label="20 Days",
        tone="pink",
        features_text="First feature\n\nSecond feature\nThird feature\n",
    )
    assert plan.feature_list == ["First feature", "Second feature", "Third feature"]
    assert plan.price_display == "$1,100"
    assert str(plan) == "Casual Day"


def test_pricing_plan_price_display_keeps_cents_when_not_whole():
    plan = PricingPlan.objects.create(
        name="Half Day", dog_count=1, price="47.50", period_label="1 Day", features_text="x"
    )
    assert plan.price_display == "$47.5"


def test_team_member_str():
    member = TeamMember.objects.create(name="Karen", bio="<p>Loves dogs.</p>")
    assert str(member) == "Karen"


def test_site_settings_is_a_singleton():
    first = SiteSettings.load()
    first.phone = "(02) 9999 0000"
    first.save()
    second = SiteSettings.load()
    assert second.pk == first.pk == 1
    assert second.phone == "(02) 9999 0000"
    assert SiteSettings.objects.count() == 1
