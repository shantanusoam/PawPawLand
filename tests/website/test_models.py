import pytest

from website.models import FAQ, Service, Testimonial

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
