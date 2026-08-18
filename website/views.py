from django.shortcuts import render

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


def _stub(request, title):
    return render(request, "website/page_stub.html", {"title": title})


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


def gallery(request):
    context = {"images": GalleryImage.objects.filter(is_active=True)}
    return render(request, "website/gallery.html", context)


def contact(request):
    return _stub(request, "Contact Us")
