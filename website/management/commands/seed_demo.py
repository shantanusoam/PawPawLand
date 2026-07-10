"""Seed demo content matching the Paw Paw Land Figma design. Idempotent."""

from pathlib import Path

from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand

from website.models import FAQ, GalleryImage, Service, Testimonial

STATIC_IMG = Path(settings.BASE_DIR) / "website" / "static" / "img"

SERVICES = [
    {
        "name": "Dog Daycare",
        "slug": "dog-daycare",
        "emoji_badge": "☀️",
        "image": "service-daycare.webp",
        "description": (
            "<p>Full day of supervised play, socialisation, exercise, "
            "and rest in a safe, loving environment.</p>"
        ),
        "price_label": "From $45/day",
    },
    {
        "name": "Dog Grooming",
        "slug": "dog-grooming",
        "emoji_badge": "✂️",
        "image": "service-grooming.webp",
        "description": (
            "<p>Bath, nail trim, coat brush, ear cleaning, and breed-specific "
            "styling by our professional groomers.</p>"
        ),
        "price_label": "From $65/session",
    },
    {
        "name": "Puppy Playground",
        "slug": "puppy-playground",
        "emoji_badge": "🐶",
        "image": "service-puppy.webp",
        "description": (
            "<p>A gentle, age-appropriate zone where puppies learn to socialise, "
            "explore, and build confidence safely.</p>"
        ),
        "price_label": "From $40/session",
    },
    {
        "name": "Dog Birthday Parties",
        "slug": "dog-birthday-parties",
        "emoji_badge": "🎂",
        "image": "service-parties.webp",
        "description": (
            "<p>Private celebrations with decorations, dog-safe treats, playtime, "
            "and photos your pup will never forget.</p>"
        ),
        "price_label": "From $120/party",
    },
]

TESTIMONIALS = [
    {
        "author_name": "Sarah Mitchell",
        "dog_name": "Biscuit the Golden",
        "avatar": "avatar-sarah.webp",
        "quote": (
            "<p>“Paw Paw Land has been a game-changer for us. Biscuit comes home "
            "absolutely exhausted and happy every single day. I love knowing he's in "
            "safe, loving hands!”</p>"
        ),
        "rating": 5,
    },
    {
        "author_name": "James Nguyen",
        "dog_name": "Mochi the Shiba",
        "avatar": "",
        "quote": (
            "<p>“The groomers here are magicians. Mochi used to hate bath time, "
            "now she practically drags me through the door. Highly recommend!”</p>"
        ),
        "rating": 5,
    },
    {
        "author_name": "Priya Sharma",
        "dog_name": "Ollie the Collie",
        "avatar": "",
        "quote": (
            "<p>“We booked Ollie's fifth birthday party here and it was the "
            "highlight of his year. The photos alone were worth it.”</p>"
        ),
        "rating": 5,
    },
]

FAQS = [
    {
        "question": "What does my dog need before their first visit?",
        "answer": (
            "<p>All dogs need up-to-date vaccinations (C5), flea and worm treatment, and a "
            "short temperament meet-and-greet before their first full day. Bring their usual "
            "food if they're staying over lunch — we handle the rest, including water, "
            "treats, and plenty of belly rubs.</p>"
        ),
    },
    {
        "question": "How are play groups organised during daycare?",
        "answer": (
            "<p>Dogs are grouped by size, age, and play style — never just thrown together. "
            "Our carers rotate structured play, quiet time, and rest so every dog gets a "
            "balanced, happy day.</p>"
        ),
    },
    {
        "question": "Can I watch my dog during the day?",
        "answer": (
            "<p>Yes! We send photo updates through the day, and you're welcome to call any "
            "time. Pick-up staff will give you a full rundown of who your pup played with "
            "and how they went.</p>"
        ),
    },
    {
        "question": "What happens if my dog doesn't settle in?",
        "answer": (
            "<p>Some dogs need a slower start, and that's okay. We'll design a gradual "
            "settling-in plan — shorter visits, quieter groups, one-on-one time — and keep "
            "you in the loop at every step.</p>"
        ),
    },
]

# Gallery photos: (static filename, alt text, row)
GALLERY = [
    ("gallery-01.webp", "Fluffy dog smiling at the camera", 1),
    ("gallery-02.webp", "Golden Spaniel relaxing in the play area", 1),
    ("gallery-03.webp", "Black dog exploring the yard", 1),
    ("gallery-04.webp", "Golden Retriever out on a walk", 1),
    ("gallery-05.webp", "Pup conquering the agility course", 1),
    ("gallery-06.webp", "Sheepdog hanging out with friends", 1),
    ("gallery-07.webp", "Playtime in the outdoor run", 2),
    ("gallery-08.webp", "Black Labrador enjoying the sunshine", 2),
    ("gallery-09.webp", "Doggy friends at the daycare", 2),
    ("gallery-10.webp", "Happy pup at the end of the day", 2),
    ("gallery-11.webp", "Border Collie celebrating a birthday", 2),
]


class Command(BaseCommand):
    help = "Seed demo services, testimonials, FAQs and gallery images (idempotent)."

    def _attach_image(self, instance, field_name, filename):
        field = getattr(instance, field_name)
        if not filename or field:
            return False
        path = STATIC_IMG / filename
        if not path.exists():
            self.stderr.write(f"  missing static image: {path}")
            return False
        with path.open("rb") as fh:
            field.save(filename, File(fh), save=False)
        return True

    def handle(self, *args, **options):
        for i, data in enumerate(SERVICES):
            image = data["image"]
            defaults = {k: v for k, v in data.items() if k != "image"}
            service, created = Service.objects.get_or_create(
                slug=data["slug"], defaults={**defaults, "sort_order": i}
            )
            if self._attach_image(service, "image", image) or created:
                service.save()
            self.stdout.write(f"Service: {service.name} ({'created' if created else 'exists'})")

        for i, data in enumerate(TESTIMONIALS):
            avatar = data["avatar"]
            defaults = {k: v for k, v in data.items() if k != "avatar"}
            testimonial, created = Testimonial.objects.get_or_create(
                author_name=data["author_name"], defaults={**defaults, "sort_order": i}
            )
            if self._attach_image(testimonial, "avatar", avatar) or created:
                testimonial.save()
            self.stdout.write(
                f"Testimonial: {testimonial.author_name} ({'created' if created else 'exists'})"
            )

        for i, data in enumerate(FAQS):
            faq, created = FAQ.objects.get_or_create(
                question=data["question"], defaults={**data, "sort_order": i}
            )
            self.stdout.write(f"FAQ: {faq.question} ({'created' if created else 'exists'})")

        for i, (filename, alt_text, row) in enumerate(GALLERY):
            photo, created = GalleryImage.objects.get_or_create(
                alt_text=alt_text, defaults={"row": row, "sort_order": i}
            )
            if self._attach_image(photo, "image", filename) or created:
                photo.save()
            self.stdout.write(f"Gallery: {alt_text} ({'created' if created else 'exists'})")

        self.stdout.write(self.style.SUCCESS("Demo content seeded."))
