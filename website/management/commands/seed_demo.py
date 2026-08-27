"""Seed demo content matching the Paw Paw Land Figma design. Idempotent."""

from pathlib import Path

from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand

from website.models import (
    FAQ,
    GalleryImage,
    PricingPlan,
    Service,
    SiteSettings,
    TeamMember,
    Testimonial,
)

STATIC_IMG = Path(settings.BASE_DIR) / "website" / "static" / "img"

SERVICES = [
    {
        "name": "Dog Daycare",
        "slug": "dog-daycare",
        "emoji_badge": "☀️",
        "image": "card-daycare-dog.webp",
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
        "image": "card-grooming-dog.webp",
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
        "image": "card-puppy-dog.webp",
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
        "image": "card-parties-dog.webp",
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

PRICING_PLANS = [
    {
        "name": "Casual Day",
        "dog_count": 1,
        "photo": "pup-corgi.webp",
        "price": "65.00",
        "period_label": "1 Day",
        "tone": "blue",
        "features_text": (
            "Perfect for occasional daycare\n"
            "Full day of supervised care\n"
            "Play, socialisation & enrichment\n"
            "Safe spaces for rest & relaxation\n"
            "No long-term commitment"
        ),
    },
    {
        "name": "Value Pack",
        "dog_count": 1,
        "photo": "pup-golden.webp",
        "price": "305.00",
        "period_label": "10 Days",
        "tone": "gold",
        "features_text": (
            "Ideal for regular daycare visits\n"
            "Flexible use across 10 daycare days\n"
            "Valid for 6 months from purchase\n"
            "Consistent routine & socialisation\n"
            "Keep your pup active & happy"
        ),
    },
    {
        "name": "Paw-some Plan",
        "dog_count": 1,
        "photo": "pup-bordercollie.webp",
        "price": "1100.00",
        "period_label": "20 Days",
        "tone": "pink",
        "features_text": (
            "Best for frequent daycare needs\n"
            "Flexible use across 20 daycare days\n"
            "Valid for 12 months from purchase\n"
            "Consistent care, play & enrichment\n"
            "Best long-term value for regular pups"
        ),
    },
    {
        "name": "Double Paw Day",
        "dog_count": 2,
        "photo": "pair-corgi-golden.webp",
        "price": "110.00",
        "period_label": "1 Day",
        "tone": "mint",
        "features_text": (
            "Full day of supervised daycare\n"
            "$55/day per dog\n"
            "Safe, playful & social environment\n"
            "Play, enrichment & downtime\n"
            "Socialisation with compatible pups"
        ),
    },
    {
        "name": "Paws & Play Pack",
        "dog_count": 2,
        "photo": "pair-samoyed-golden.webp",
        "price": "1000.00",
        "period_label": "10 Days",
        "tone": "gold",
        "features_text": (
            "10 full days of daycare\n"
            "$50/day per dog • Valid 6 months\n"
            "Consistent routine & socialisation\n"
            "Supervised play & enrichment\n"
            "Plenty of rest & relaxation"
        ),
    },
    {
        "name": "Ultimate Paw Pack",
        "dog_count": 2,
        "photo": "pair-poodle-collie.webp",
        "price": "1900.00",
        "period_label": "20 Days",
        "tone": "pink",
        "features_text": (
            "20 full days of daycare\n"
            "$47.50/day per dog • Valid 12 months\n"
            "Best value for regular pups\n"
            "Daily play & enrichment\n"
            "Consistent care & social time"
        ),
    },
]

TEAM_MEMBERS = [
    {
        "name": "Karen",
        "role": "Puppy Specialist",
        "photo": "team-karen.webp",
        "bio": (
            "<p>I love working with dogs! I have worked with dogs for over 15 years in the "
            "dog training and dog daycare industries.</p>"
            "<p>I love working at Pawpaw Land because we build such a wonderful relationship "
            "with each of the dogs, it makes coming to work a pleasure.</p>"
            "<p>I have a Labrador named Sage and I am very lucky to be able to bring Sage to "
            "work with me here at Pawpaw Land.</p>"
        ),
    },
    {
        "name": "Leah",
        "role": "Puppy Specialist",
        "photo": "team-leah.webp",
        "bio": (
            "<p>I have been working with dogs for just over 3 years in day care and kennel "
            "settings, but have been working in the animal industry for over 10 years!</p>"
            "<p>I don't have any dogs at home so my favourite part of my job is getting to "
            "see all the beautiful dogs and treating them all like they're my own.</p>"
            "<p>A fun fact about me is my animal experience started with crocodiles, snakes "
            "and stingrays at Crocosaurus Cove in Darwin!</p>"
        ),
    },
]

SITE_SETTINGS = {
    "phone": "(02) 9123 4567",
    "email": "hello@pawpawland.com.au",
    "address_line": "123 Happy Paws Lane, Sydney NSW 2000",
    "hours_weekday": "Mon–Fri: 7am–6pm",
    "hours_weekend": "Sat–Sun: 8am–4pm",
    "facebook_url": "",
    "instagram_url": "",
}

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
        if not filename:
            return False
        if field and Path(field.name).name == filename:
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

        for i, data in enumerate(PRICING_PLANS):
            photo = data["photo"]
            defaults = {k: v for k, v in data.items() if k != "photo"}
            plan, created = PricingPlan.objects.get_or_create(
                name=data["name"], defaults={**defaults, "sort_order": i}
            )
            if self._attach_image(plan, "photo", photo) or created:
                plan.save()
            self.stdout.write(f"Pricing plan: {plan.name} ({'created' if created else 'exists'})")

        for i, data in enumerate(TEAM_MEMBERS):
            photo = data["photo"]
            defaults = {k: v for k, v in data.items() if k != "photo"}
            member, created = TeamMember.objects.get_or_create(
                name=data["name"], defaults={**defaults, "sort_order": i}
            )
            if self._attach_image(member, "photo", photo) or created:
                member.save()
            self.stdout.write(f"Team member: {member.name} ({'created' if created else 'exists'})")

        settings_obj = SiteSettings.load()
        if not settings_obj.phone and not settings_obj.email:
            for key, value in SITE_SETTINGS.items():
                setattr(settings_obj, key, value)
            settings_obj.save()
            self.stdout.write("Site settings: seeded")
        else:
            self.stdout.write("Site settings: exists")

        self.stdout.write(self.style.SUCCESS("Demo content seeded."))
