import logging

from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ContactForm, RegistrationForm
from .models import (
    FAQ,
    GalleryImage,
    LegalPage,
    PricingPlan,
    Service,
    SiteSettings,
    TeamMember,
    Testimonial,
)

logger = logging.getLogger(__name__)


def _notify(subject, lines):
    """Email a plain-text notification to SiteSettings.email. Never raises —
    a down mail server shouldn't stop a visitor's form submission from saving."""
    recipient = SiteSettings.load().email
    if not recipient:
        return
    try:
        send_mail(
            subject,
            "\n".join(lines),
            None,
            [recipient],
            fail_silently=False,
        )
    except Exception:
        logger.exception("Failed to send notification email: %s", subject)


# Accent tones cycled across service cards / FAQ rows / team cards, matching the Figma palette.
SERVICE_TONES = [
    {"badge": "bg-gold", "button": "bg-gold text-ink"},
    {"badge": "bg-blue-soft", "button": "bg-blue-soft text-ink"},
    {"badge": "bg-pink-pastel", "button": "bg-pink-pastel text-ink"},
    {"badge": "bg-navy", "button": "bg-navy text-white"},
]
FAQ_TONES = ["bg-pink-soft", "bg-blue-pastel", "bg-[#f9d292]", "bg-[#d2e2ee]"]
TEAM_TONES = ["bg-[#def0ff]", "bg-[#fbe2e7]", "bg-[#fff2c8]", "bg-[#fcf1ff]"]

# Card colors per pricing plan tone (chosen per-plan in admin).
PLAN_TONES = {
    "blue": {
        "bg": "bg-[#f5f9fb]",
        "border": "border-[#b7cfe7]",
        "title": "text-[#529de1]",
        "chip": "bg-[#dfedf7]",
        "check": "text-[#529de1]",
    },
    "gold": {
        "bg": "bg-[#fefbf7]",
        "border": "border-[#fbd9a1]",
        "title": "text-gold",
        "chip": "bg-[#fdf3e0]",
        "check": "text-gold",
    },
    "pink": {
        "bg": "bg-[#fef8f4]",
        "border": "border-[#fab4bb]",
        "title": "text-[#fc748c]",
        "chip": "bg-[#fdebeb]",
        "check": "text-coral",
    },
    "mint": {
        "bg": "bg-[#f5f9f7]",
        "border": "border-[#b9dad2]",
        "title": "text-[#46a48a]",
        "chip": "bg-[#e5f4ed]",
        "check": "text-[#46a48a]",
    },
}


def home(request):
    services = list(Service.objects.filter(is_active=True))
    for i, service in enumerate(services):
        service.tone = SERVICE_TONES[i % len(SERVICE_TONES)]
    faqs = list(FAQ.objects.filter(is_active=True))
    for i, faq in enumerate(faqs):
        faq.tone = FAQ_TONES[i % len(FAQ_TONES)]
    context = {
        "services": services,
        "testimonials": Testimonial.objects.filter(is_active=True),
        "faqs": faqs,
        "gallery_row_1": GalleryImage.objects.filter(is_active=True, row=1),
        "gallery_row_2": GalleryImage.objects.filter(is_active=True, row=2),
    }
    return render(request, "website/home.html", context)


def about(request):
    team_members = list(TeamMember.objects.filter(is_active=True))
    for i, member in enumerate(team_members):
        member.tone = TEAM_TONES[i % len(TEAM_TONES)]
    context = {
        "team_members": team_members,
        "gallery_row_1": GalleryImage.objects.filter(is_active=True, row=1),
        "gallery_row_2": GalleryImage.objects.filter(is_active=True, row=2),
    }
    return render(request, "website/about.html", context)


def _with_tone_style(plans):
    plans = list(plans)
    for plan in plans:
        plan.tone_style = PLAN_TONES[plan.tone]
    return plans


def services(request):
    context = {
        "services": Service.objects.filter(is_active=True),
        "gallery_row_1": GalleryImage.objects.filter(is_active=True, row=1),
        "gallery_row_2": GalleryImage.objects.filter(is_active=True, row=2),
    }
    return render(request, "website/services.html", context)


# Per-service detail page content, matching each Figma variant of the Services page.
# _GENERIC_DETAIL is the Day Care copy, reused as a last-resort fallback for any
# service slug that doesn't have its own entry below.
_GENERIC_DETAIL = {
    "eyebrow": "Our Daycare",
    "promo": None,
    "hero_heading_svg": "heading-daycare.svg",
    "hero_body": (
        "Bring your furry best friend along and join us for a fun-filled day of "
        "wagging tails, happy moments, and pawsome memories!"
    ),
    "hero_photo": "services-hero.webp",
    "intro_image": "service-daycare-intro.webp",
    "intro_heading_line1": "A Happy Day,",
    "intro_heading_highlight": "Filled With Care",
    "intro_subheading": "Not Just Daycare, It's Their Second Home",
    "intro_body": [
        "We know leaving your dog for the day isn't always easy. That's why we've "
        "created a safe, caring, and happy space where they can play, socialise, "
        "relax, and simply be themselves.",
        "With supervised play, personalised attention, plenty of cuddles, and "
        "comfortable rest time, every pup gets a day that suits their personality "
        "and energy.",
        "You go about your day worry-free. They spend theirs playing, making "
        "friends, and coming home happy.",
    ],
    "intro_button_label": "Discover Our Daycare →",
}

SERVICE_DETAIL_CONTENT = {
    "dog-daycare": _GENERIC_DETAIL,
    "dog-grooming": {
        "eyebrow": "PAW PAW's SPA",
        "promo": None,
        "hero_heading_svg": "heading-spa.svg",
        "hero_body": (
            "Treat your furry best friend to a pampering spa day filled with "
            "gentle care, fresh fluff, and plenty of tail-wagging happiness!"
        ),
        "hero_photo": "service-spa-hero.webp",
        "intro_image": "service-grooming-intro.webp",
        "intro_heading_line1": None,
        "intro_heading_plain_prefix": "A Fresh",
        "intro_heading_highlight": "New Look,",
        "intro_subheading": "A Spa Day They'll Love",
        "intro_body": [
            "We know grooming is more than just looking good. At Paw Paw's "
            "Spa, every pup gets a gentle, caring, and stress-free experience "
            "tailored to their needs.",
            "With expert grooming, gentle handling, a refreshing bath, and "
            "plenty of care, we make sure they leave feeling clean, "
            "comfortable, and looking their very best.",
            "You drop off a pup. You pick up a fresher, fluffier, happier one.",
        ],
        "intro_button_label": "Discover Our Spa →",
        "rate_card_image": "grooming-rate-card.webp",
        "cta_heading": "Ready for a fresh new look?",
        "cta_body": "Book their next spa day today. First visit? We'd love to meet your "
        "furry best friend.",
        "cta_button_label": "Schedule A Spa Day →",
    },
    "puppy-playgroup": {
        "eyebrow": "Puppy Playgroup",
        "promo": None,
        # No matching "Puppy Playgroup" heading graphic exists yet (the old asset
        # read "Puppy Playground") — render a styled text heading instead until
        # the client supplies a new one.
        "hero_heading_svg": None,
        "hero_heading_text": "Puppy Playgroup",
        "hero_body": "Little paws. Big first experiences.",
        "hero_photo": "service-puppy-hero.webp",
        "intro_image": "service-puppy-intro.webp",
        "intro_heading_line1": "Little Paws.",
        "intro_heading_highlight": "Big First Experiences",
        "intro_subheading": "Socialisation, tailored to your puppy",
        "intro_body": [
            "The first few months of a puppy's life are an important time for "
            "learning about the world around them. Our Puppy Playgroup provides "
            "young puppies with positive, carefully managed social experiences "
            "during this formative stage, helping build the foundations for a "
            "confident, well-adjusted adult dog.",
            "Every puppy is different. Some are naturally outgoing and playful, "
            "while others need a little more time and reassurance.",
            "We tailor each puppy's experience to their temperament and "
            "confidence, gradually introducing them to carefully matched puppies "
            "and, where appropriate, calm adult dogs. Rather than simply letting "
            "puppies play together, our focus is on structured, closely "
            "monitored socialisation in a nurturing environment.",
        ],
        "intro_body_more": [
            "Sessions may include supervised play, enrichment and "
            "confidence-building activities, positive reinforcement, exposure to "
            "new sounds and experiences, and plenty of rest in between. A "
            "dedicated daycare attendant monitors the group throughout the "
            "session, with updates on how your puppy is progressing.",
            "Designed especially for young puppies during their early "
            "socialisation period. Places are kept limited so we can carefully "
            "match puppies and give each one the attention and support they "
            "need.",
            "Positive early experiences. Happy little puppies. Confident dogs in the making.",
        ],
        # No CTA button here per client feedback ("Remove Discover Puppy Play").
        "cta_heading": "Ready for their first playdate?",
        "cta_body": "Book your puppy's next playgroup session today. We'd love to meet "
        "your little pup.",
        "cta_button_label": "Schedule A Playdate →",
    },
    "dog-birthday-parties": {
        "eyebrow": "Dog Birthday Party",
        "promo": None,
        "hero_heading_svg": "heading-party.svg",
        "hero_body": (
            "Celebrate your furry best friend's special day with a fun-filled "
            "party of wagging tails, playful moments, tasty treats, and pawsome "
            "memories!"
        ),
        "hero_photo": "service-party-hero.webp",
        "intro_image": "service-party-intro.webp",
        "intro_heading_line1": None,
        "intro_heading_highlight_prefix": "A Party",
        "intro_heading_suffix": "They'll Love,",
        "intro_subheading": "A Celebration They'll Never Forget",
        "intro_body": [
            "We know your dog is more than just a pet — they're family. That's "
            "why we create fun, joyful, and tail-wagging celebrations where every "
            "pup can play, socialise, and enjoy their special day.",
            "With playtime, pup-friendly treats, personalised touches, and "
            "plenty of happy moments, every party is made to suit your dog's "
            "personality and bring their favourite furry friends together.",
            "You bring the birthday pup. We'll bring the fun, the memories, and "
            "a whole lot of wagging tails.",
        ],
        "intro_button_label": "Discover Parties →",
        "cta_heading": "Ready to plan their party?",
        "cta_body": "Book your pup's birthday celebration today. Let's make it pawsome.",
        "cta_button_label": "Schedule A Party →",
    },
}
# Day Care gets its own promo line and navy (not gold) hero heading treatment.
SERVICE_DETAIL_CONTENT["dog-daycare"] = {
    **_GENERIC_DETAIL,
    "promo": "First 3 sessions for $75*",
}


def service_detail(request, slug):
    service = get_object_or_404(Service, slug=slug, is_active=True)
    detail = SERVICE_DETAIL_CONTENT.get(slug, _GENERIC_DETAIL)
    plans_one_dog = _with_tone_style(
        PricingPlan.objects.filter(is_active=True, dog_count=1, service=service)
    )
    plans_two_dogs = _with_tone_style(
        PricingPlan.objects.filter(is_active=True, dog_count=2, service=service)
    )
    plans_three_dogs = _with_tone_style(
        PricingPlan.objects.filter(is_active=True, dog_count=3, service=service)
    )
    context = {
        "service": service,
        "detail": detail,
        "pricing_service": service,
        "plans_one_dog": plans_one_dog,
        "plans_two_dogs": plans_two_dogs,
        "plans_three_dogs": plans_three_dogs,
        "gallery_images": GalleryImage.objects.filter(is_active=True, service=service),
    }
    return render(request, "website/service_detail.html", context)


def gallery(request):
    context = {"images": GalleryImage.objects.filter(is_active=True).select_related("service")}
    return render(request, "website/gallery.html", context)


def service_gallery(request, slug):
    service = get_object_or_404(Service, slug=slug, is_active=True)
    context = {
        "service": service,
        "images": GalleryImage.objects.filter(is_active=True, service=service),
    }
    return render(request, "website/service_gallery.html", context)


def legal_page(request, slug):
    page = get_object_or_404(LegalPage, slug=slug)
    return render(request, "website/legal_page.html", {"page": page})


def contact(request):
    service_choices = [(svc.name, svc.name) for svc in Service.objects.filter(is_active=True)]
    if request.method == "POST":
        form = ContactForm(request.POST, service_choices=service_choices)
        if form.is_valid():
            submission = form.save()
            _notify(
                f"New Contact Form Submission — {submission.full_name}",
                [
                    f"Name: {submission.full_name}",
                    f"Email: {submission.email}",
                    f"Phone: {submission.phone}",
                    f"Service requested: {submission.service_requested}",
                    "",
                    "Message:",
                    submission.message,
                ],
            )
            messages.success(
                request, "Thanks! We've got your message and will be in touch shortly."
            )
            return redirect("website:contact")
    else:
        form = ContactForm(service_choices=service_choices)
    return render(request, "website/contact.html", {"form": form})


def registration(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            reg = form.save()
            lines = [
                f"Owner: {reg.owner_name}",
                f"Address: {reg.address}, {reg.suburb} {reg.postcode}",
                f"Phone: {reg.phone}",
                f"Email: {reg.email}",
                "",
                f"Emergency contact: {reg.emergency_contact_name} ({reg.emergency_contact_phone})",
                f"Vet: {reg.vet_clinic_name} ({reg.vet_phone})",
                "",
                f"Dog's name: {reg.dog_name}",
                f"Microchip: {reg.microchip_number}",
                f"Breed: {reg.breed}",
                f"Colour: {reg.colour}",
                f"Date of birth: {reg.date_of_birth}",
                f"Gender: {reg.get_gender_display()}",
                f"Desexed: {reg.get_is_desexed_display()}",
                f"Aggression to dogs/people: {reg.get_has_aggression_display()}",
            ]
            if reg.aggression_details:
                lines.append(f"  Details: {reg.aggression_details}")
            lines.append(f"Last vaccination date: {reg.last_vaccination_date}")
            lines.append(f"Health ailments: {reg.get_has_health_ailments_display()}")
            if reg.health_ailments_details:
                lines.append(f"  Details: {reg.health_ailments_details}")
            lines.append(f"Medication: {reg.get_has_medication_display()}")
            if reg.medication_details:
                lines.append(f"  Details: {reg.medication_details}")
            if reg.food_allergies:
                lines += ["", f"Food allergies: {reg.food_allergies}"]
            if reg.instagram_handle:
                lines.append(f"Instagram: {reg.instagram_handle}")
            if reg.heard_about:
                lines.append(f"Heard about us: {reg.heard_about}")
                if reg.heard_about_other:
                    lines.append(f"  Other: {reg.heard_about_other}")
            _notify(f"New Dog Registration — {reg.dog_name} ({reg.owner_name})", lines)
            messages.success(request, "Thanks! Your dog's registration has been received.")
            return redirect("website:registration")
    else:
        form = RegistrationForm()
    return render(request, "website/registration.html", {"form": form})


def refer(request):
    return render(request, "website/refer.html")
