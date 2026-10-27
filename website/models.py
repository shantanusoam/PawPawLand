from datetime import date
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

    # Pricing-section taglines, one plain/gold-highlight pair per dog-count grid.
    # Each pair defaults to the site's original copy when left blank, so existing
    # services don't need any admin changes to keep their current heading.
    tagline_1dog_plain = models.CharField(
        max_length=80,
        blank=True,
        help_text='Plain part of the "1 dog" pricing heading. '
        'Defaults to "Give Your Pup More Play &" when blank.',
    )
    tagline_1dog_gold = models.CharField(
        max_length=80,
        blank=True,
        help_text='Gold-highlighted part of the "1 dog" pricing heading. '
        'Defaults to "Save More!" when blank.',
    )
    tagline_2dogs_plain = models.CharField(
        max_length=80,
        blank=True,
        help_text='Plain part of the "2 dogs" pricing heading. Defaults to "Two Pups," when blank.',
    )
    tagline_2dogs_gold = models.CharField(
        max_length=80,
        blank=True,
        help_text='Gold-highlighted part of the "2 dogs" pricing heading. '
        'Defaults to "Twice the Happiness!" when blank.',
    )
    tagline_3dogs_plain = models.CharField(
        max_length=80,
        blank=True,
        help_text='Plain part of the "3 dogs" pricing heading. '
        'Defaults to "Three Pups," when blank.',
    )
    tagline_3dogs_gold = models.CharField(
        max_length=80,
        blank=True,
        help_text='Gold-highlighted part of the "3 dogs" pricing heading. '
        'Defaults to "Triple the Tail Wags!" when blank.',
    )

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
    service = models.ForeignKey(
        "Service",
        on_delete=models.CASCADE,
        related_name="gallery_images",
        null=True,
        blank=True,
        help_text="Leave blank to show only on the main Gallery page. Set this to also "
        "show the photo on that service's own gallery.",
    )

    def __str__(self):
        return self.alt_text


class PricingPlan(OrderedActiveModel):
    DOG_COUNT_CHOICES = [(1, "1 dog"), (2, "2 dogs"), (3, "3 dogs")]
    TONE_CHOICES = [
        ("blue", "Blue"),
        ("gold", "Gold"),
        ("pink", "Pink"),
        ("mint", "Mint"),
    ]

    name = models.CharField(max_length=100, help_text='e.g. "Casual Day"')
    service = models.ForeignKey(
        "Service",
        on_delete=models.CASCADE,
        related_name="pricing_plans",
        null=True,
        blank=True,
        help_text="Which service this plan's prices belong to. Leave blank to show on "
        "every service's page (legacy behaviour).",
    )
    dog_count = models.PositiveSmallIntegerField(
        choices=DOG_COUNT_CHOICES, default=1, help_text="Which pricing grid this plan appears in"
    )
    photo = models.ImageField(upload_to="pricing/", blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    period_label = models.CharField(max_length=30, help_text='e.g. "1 Day", "10 Days"')
    price_caption = models.CharField(
        max_length=120,
        blank=True,
        help_text='Short caption under this price, e.g. "Ideal for shorter visits". '
        "Only shown when Price 2 is also set.",
    )
    price_2 = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Optional second price — fill this in to show a split price card "
        "(e.g. Half-Day vs Session) instead of the single price above.",
    )
    period_label_2 = models.CharField(
        max_length=30, blank=True, help_text='e.g. "Session" — only used when Price 2 is set.'
    )
    price_2_caption = models.CharField(
        max_length=120, blank=True, help_text="Short caption under the second price."
    )
    price_3 = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Optional third price — only used when Price 2 is also set, for a "
        "three-way split (e.g. Half-Day / Session / Full Week).",
    )
    period_label_3 = models.CharField(
        max_length=30, blank=True, help_text="Only used when Price 3 is set."
    )
    price_3_caption = models.CharField(
        max_length=120, blank=True, help_text="Short caption under the third price."
    )
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

    @property
    def is_dual_price(self):
        return self.price_2 is not None

    @property
    def price_2_display(self):
        if self.price_2 is None:
            return ""
        formatted = f"{Decimal(self.price_2):,.2f}".rstrip("0").rstrip(".")
        return f"${formatted}"

    @property
    def is_triple_price(self):
        return self.price_2 is not None and self.price_3 is not None

    @property
    def price_3_display(self):
        if self.price_3 is None:
            return ""
        formatted = f"{Decimal(self.price_3):,.2f}".rstrip("0").rstrip(".")
        return f"${formatted}"


class TeamMember(OrderedActiveModel):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100, default="Puppy Specialist")
    photo = models.ImageField(upload_to="team/", blank=True)
    bio = HTMLField()

    def __str__(self):
        return self.name


class LegalPage(models.Model):
    """Admin-editable static pages, e.g. Terms of Service, Privacy Policy."""

    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    body = HTMLField()

    def __str__(self):
        return self.title


class SiteSettings(models.Model):
    """Singleton: site-wide contact info and social links, editable from admin."""

    phone = models.CharField(max_length=30, blank=True)
    mobile = models.CharField(max_length=30, blank=True, help_text='e.g. "0412 345 678"')
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
    booking_url = models.URLField(
        blank=True,
        default="https://pawpawland.as.me/schedule/56746727",
        help_text="Where every 'Book Now' / 'Schedule A Visit' button on the site links to.",
    )

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


class Registration(models.Model):
    """A full dog registration submitted through the Registration page."""

    YES_NO_CHOICES = [("yes", "Yes"), ("no", "No")]
    GENDER_CHOICES = [("male", "Male"), ("female", "Female")]
    HEARD_ABOUT_CHOICES = [
        ("google", "Google"),
        ("website", "Website"),
        ("facebook", "Facebook"),
        ("instagram", "Instagram"),
        ("vet_rec", "Vet Rec."),
        ("referral", "Referral"),
        ("other", "Other"),
    ]

    # Your contact details
    owner_name = models.CharField("Owner's Name", max_length=150, default="")
    address = models.CharField(max_length=200, default="")
    suburb = models.CharField(max_length=100, default="")
    postcode = models.CharField(max_length=20, default="")
    phone = models.CharField("Phone", max_length=30, default="")
    email = models.EmailField("Email Address")

    # Emergency contact details
    emergency_contact_name = models.CharField(max_length=150, default="")
    emergency_contact_phone = models.CharField(max_length=30, default="")

    # Vet's details
    vet_clinic_name = models.CharField(max_length=150, default="")
    vet_phone = models.CharField(max_length=30, default="")

    # Dog's details
    dog_name = models.CharField("Name of Dog", max_length=100)
    microchip_number = models.CharField(max_length=50, default="")
    dog_photo = models.ImageField(upload_to="registrations/dogs/", blank=True)
    breed = models.CharField(max_length=100, default="")
    colour = models.CharField(max_length=100, default="")
    date_of_birth = models.DateField(default=date.today)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default="")
    is_desexed = models.CharField(
        "Is your dog desexed?", max_length=3, choices=YES_NO_CHOICES, default=""
    )
    has_aggression = models.CharField(
        "Does your dog display aggression to other dogs or people?",
        max_length=3,
        choices=YES_NO_CHOICES,
        default="",
    )
    aggression_details = models.TextField(blank=True)
    last_vaccination_date = models.DateField(default=date.today)
    vaccination_certificate = models.FileField(
        upload_to="registrations/vaccination-certs/", blank=True
    )
    has_health_ailments = models.CharField(
        "Does your dog suffer from any health issues?",
        max_length=3,
        choices=YES_NO_CHOICES,
        default="",
    )
    health_ailments_details = models.TextField(blank=True)
    has_medication = models.CharField(
        "Is your dog on any medication?", max_length=3, choices=YES_NO_CHOICES, default=""
    )
    medication_details = models.TextField(blank=True)

    # Paw Paw Land-specific additions
    food_allergies = models.TextField(
        blank=True,
        help_text="Any foods, ingredients or treats this dog should avoid.",
    )
    instagram_handle = models.CharField(
        max_length=100,
        blank=True,
        help_text="Optional — shared only if the owner opts in to being tagged on "
        "Instagram Stories.",
    )
    heard_about = models.CharField(
        max_length=120,
        default="",
        help_text="Comma-separated choices, e.g. 'google,instagram'.",
    )
    heard_about_other = models.CharField(
        'If "other", please specify.',
        max_length=200,
        blank=True,
    )

    # Consent
    agreed_to_terms = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.dog_name} — {self.owner_name} ({self.created_at:%Y-%m-%d})"
