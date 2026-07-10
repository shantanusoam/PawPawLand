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
