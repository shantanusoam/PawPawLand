from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ContactForm
from .models import FAQ, GalleryImage, PricingPlan, Service, TeamMember, Testimonial

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


def _marquee_duration(count):
    # Scales with card count so the scroll speed stays roughly constant
    # however many plans get added in admin later.
    return max(24, count * 10)


def services(request):
    plans_one_dog = _with_tone_style(PricingPlan.objects.filter(is_active=True, dog_count=1))
    plans_two_dogs = _with_tone_style(PricingPlan.objects.filter(is_active=True, dog_count=2))
    context = {
        "services": Service.objects.filter(is_active=True),
        "plans_one_dog": plans_one_dog,
        "plans_one_dog_duration": _marquee_duration(len(plans_one_dog)),
        "plans_two_dogs": plans_two_dogs,
        "plans_two_dogs_duration": _marquee_duration(len(plans_two_dogs)),
    }
    return render(request, "website/services.html", context)


# Per-service detail page content, matching each Figma variant of the Services page.
# "dog-grooming" has no Figma design yet, so it falls back to the generic Meet & Greet
# copy the other three originally shared — swap in real content once that design exists.
_GENERIC_DETAIL = {
    "eyebrow": "Our Daycare",
    "promo": None,
    "hero_heading_svg": "heading-daycare.svg",
    "hero_body": (
        "Bring your furry best friend along and join us for a fun-filled day of "
        "wagging tails, happy moments, and pawsome memories!"
    ),
    "hero_photo": "services-hero.webp",
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
    "dog-grooming": _GENERIC_DETAIL,
    "puppy-playground": {
        "eyebrow": "Puppy Playground",
        "promo": None,
        "hero_heading_svg": "heading-puppy-playground.svg",
        "hero_body": (
            "Let your little pup explore, play, make new friends, and enjoy a "
            "fun-filled day made just for tiny paws and big adventures!"
        ),
        "hero_photo": "service-puppy-hero.webp",
        "intro_heading_line1": "A Little Adventure",
        "intro_heading_highlight": "They'll Love,",
        "intro_subheading": "A Playground Made Just for Pups",
        "intro_body": [
            "We know puppies need more than just space to run — they need a safe, "
            "playful, and nurturing environment where they can explore, learn, and "
            "grow with confidence.",
            "With supervised play, gentle socialisation, fun enrichment, and "
            "plenty of rest, every little pup gets to enjoy playtime at their own "
            "pace.",
            "They explore, make new friends, build confidence, and head home "
            "happy, tired, and ready for a nap.",
        ],
        "intro_button_label": "Discover Puppy Play →",
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
    plans_one_dog = _with_tone_style(PricingPlan.objects.filter(is_active=True, dog_count=1))
    plans_two_dogs = _with_tone_style(PricingPlan.objects.filter(is_active=True, dog_count=2))
    context = {
        "service": service,
        "detail": detail,
        "plans_one_dog": plans_one_dog,
        "plans_one_dog_duration": _marquee_duration(len(plans_one_dog)),
        "plans_two_dogs": plans_two_dogs,
        "plans_two_dogs_duration": _marquee_duration(len(plans_two_dogs)),
    }
    return render(request, "website/service_detail.html", context)


def gallery(request):
    context = {"images": GalleryImage.objects.filter(is_active=True)}
    return render(request, "website/gallery.html", context)


def contact(request):
    service_choices = [(svc.name, svc.name) for svc in Service.objects.filter(is_active=True)]
    if request.method == "POST":
        form = ContactForm(request.POST, service_choices=service_choices)
        if form.is_valid():
            form.save()
            messages.success(
                request, "Thanks! We've got your message and will be in touch shortly."
            )
            return redirect("website:contact")
    else:
        form = ContactForm(service_choices=service_choices)
    return render(request, "website/contact.html", {"form": form})
