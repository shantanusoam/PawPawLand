from django.shortcuts import render

from .models import FAQ, GalleryImage, Service, Testimonial

# Accent tones cycled across service cards / FAQ rows, matching the Figma palette.
SERVICE_TONES = [
    {"badge": "bg-gold", "button": "bg-gold text-ink"},
    {"badge": "bg-blue-soft", "button": "bg-blue-soft text-ink"},
    {"badge": "bg-pink-pastel", "button": "bg-pink-pastel text-ink"},
    {"badge": "bg-navy", "button": "bg-navy text-white"},
]
FAQ_TONES = ["bg-pink-soft", "bg-blue-pastel", "bg-[#f9d292]", "bg-[#d2e2ee]"]


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
    return _stub(request, "About Us")


def services(request):
    return _stub(request, "Our Services")


def gallery(request):
    return _stub(request, "Gallery")


def contact(request):
    return _stub(request, "Contact Us")
