from decimal import Decimal

from django.db import models
from tinymce.models import HTMLField


class OrderedActiveModel(models.Model):
    """Shared ordering/visibility controls for admin-managed content."""

    sort_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True
        ordering = ["sort_order", "pk"]


class Service(OrderedActiveModel):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    emoji_badge = models.CharField(max_length=8, help_text="Emoji shown on the card, e.g. ☀️")
    image = models.ImageField(upload_to="services/", blank=True)
    description = HTMLField()
    price_label = models.CharField(max_length=50, help_text='e.g. "From $45/day"')

    def __str__(self):
        return self.name


class Testimonial(OrderedActiveModel):
    author_name = models.CharField(max_length=100)
    dog_name = models.CharField(max_length=100, help_text='e.g. "Biscuit the Golden"')
    avatar = models.ImageField(upload_to="testimonials/", blank=True)
    quote = HTMLField()
    rating = models.PositiveSmallIntegerField(
        default=5, choices=[(i, f"{i} star{'s' if i > 1 else ''}") for i in range(1, 6)]
    )

    def __str__(self):
        return f"{self.author_name} ({self.dog_name})"


class FAQ(OrderedActiveModel):
    question = models.CharField(max_length=200)
    answer = HTMLField()

    class Meta(OrderedActiveModel.Meta):
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"

    def __str__(self):
        return self.question


class GalleryImage(OrderedActiveModel):
    ROW_CHOICES = [(1, "Row 1"), (2, "Row 2")]

    image = models.ImageField(upload_to="gallery/")
    alt_text = models.CharField(max_length=200)
    row = models.PositiveSmallIntegerField(choices=ROW_CHOICES, default=1)

    def __str__(self):
        return self.alt_text


class PricingPlan(OrderedActiveModel):
    DOG_COUNT_CHOICES = [(1, "1 dog"), (2, "2 dogs")]
    TONE_CHOICES = [
        ("blue", "Blue"),
        ("gold", "Gold"),
        ("pink", "Pink"),
        ("mint", "Mint"),
    ]

    name = models.CharField(max_length=100, help_text='e.g. "Casual Day"')
    dog_count = models.PositiveSmallIntegerField(
        choices=DOG_COUNT_CHOICES, default=1, help_text="Which pricing grid this plan appears in"
    )
    photo = models.ImageField(upload_to="pricing/", blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    period_label = models.CharField(max_length=30, help_text='e.g. "1 Day", "10 Days"')
    tone = models.CharField(max_length=10, choices=TONE_CHOICES, default="blue")
    features_text = models.TextField(help_text="One feature per line.")

    def __str__(self):
        return self.name

    @property
    def feature_list(self):
        return [line.strip() for line in self.features_text.splitlines() if line.strip()]

    @property
    def price_display(self):
        formatted = f"{Decimal(self.price):,.2f}".rstrip("0").rstrip(".")
        return f"${formatted}"


class TeamMember(OrderedActiveModel):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100, default="Puppy Specialist")
    photo = models.ImageField(upload_to="team/", blank=True)
    bio = HTMLField()

    def __str__(self):
        return self.name


class SiteSettings(models.Model):
    """Singleton: site-wide contact info and social links, editable from admin."""

    phone = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)
    address_line = models.CharField(max_length=200, blank=True)
    hours_weekday = models.CharField(
        max_length=100, blank=True, help_text='e.g. "Mon–Fri: 7am–6pm"'
    )
    hours_weekend = models.CharField(
        max_length=100, blank=True, help_text='e.g. "Sat–Sun: 8am–4pm"'
    )
    facebook_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)

    class Meta:
        verbose_name = "Site settings"
        verbose_name_plural = "Site settings"

    def __str__(self):
        return "Site settings"

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class ContactSubmission(models.Model):
    """A message sent through the Contact Us form."""

    full_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=30, blank=True)
    service_requested = models.CharField(max_length=100, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.full_name} ({self.created_at:%Y-%m-%d})"
