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


# Team bios for the About page, matching the Figma copy verbatim.
_KAREN_BIO = (
    "I love working with dogs! I have worked with dogs for over 15 years in the dog "
    "training and dog daycare industries.\n\n"
    "I love working at Pawpaw Land because we build such a wonderful relationship with "
    "each of the dogs, it makes coming to work a pleasure.\n\n"
    "I have a Labrador named Sage and I am very lucky to be able to bring Sage to work "
    "with me here at Pawpaw Land."
)
_LEAH_BIO = (
    "I have been working with dogs for just over 3 years in day care and kennel "
    "settings, but have been working in the animal industry for over 10 years!\n\n"
    "I don't have any dogs at home so my favourite part of my job is getting to see all "
    "the beautiful dogs and treating them all like they're my own.\n\n"
    "A fun fact about me is my animal experience started with crocodiles, snakes and "
    "stingrays at Crocosaurus Cove in Darwin!"
)

TEAM_MEMBERS = [
    {
        "name": "Karen",
        "role": "Puppy Specialist",
        "photo": "team-karen.webp",
        "bio": _KAREN_BIO,
        "tone": "bg-[#def0ff]",
    },
    {
        "name": "Leah",
        "role": "Puppy Specialist",
        "photo": "team-leah.webp",
        "bio": _LEAH_BIO,
        "tone": "bg-[#fbe2e7]",
    },
    {
        "name": "Karen",
        "role": "Puppy Specialist",
        "photo": "team-karen.webp",
        "bio": _KAREN_BIO,
        "tone": "bg-[#fff2c8]",
    },
    {
        "name": "Leah",
        "role": "Puppy Specialist",
        "photo": "team-leah.webp",
        "bio": _LEAH_BIO,
        "tone": "bg-[#fcf1ff]",
    },
]


def about(request):
    context = {
        "team_members": TEAM_MEMBERS,
        "gallery_row_1": GalleryImage.objects.filter(is_active=True, row=1),
        "gallery_row_2": GalleryImage.objects.filter(is_active=True, row=2),
    }
    return render(request, "website/about.html", context)


# Pricing plan copy for the Services page, mirroring the Figma design 1:1.
# Tones bundle the card's bg/border/chip colors, accent text color, and check-icon color.
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

PLANS_ONE_DOG = [
    {
        "name": "Casual Day",
        "photo": "pup-corgi.webp",
        "price": "$65",
        "period": "/ 1 Day",
        "tone": PLAN_TONES["blue"],
        "features": [
            "Perfect for occasional daycare",
            "Full day of supervised care",
            "Play, socialisation & enrichment",
            "Safe spaces for rest & relaxation",
            "No long-term commitment",
        ],
    },
    {
        "name": "Value Pack",
        "photo": "pup-golden.webp",
        "price": "$305",
        "period": "/ 10 Days",
        "tone": PLAN_TONES["gold"],
        "features": [
            "Ideal for regular daycare visits",
            "Flexible use across 10 daycare days",
            "Valid for 6 months from purchase",
            "Consistent routine & socialisation",
            "Keep your pup active & happy",
        ],
    },
    {
        "name": "Paw-some Plan",
        "photo": "pup-bordercollie.webp",
        "price": "$1,100",
        "period": "/ 20 Days",
        "tone": PLAN_TONES["pink"],
        "features": [
            "Best for frequent daycare needs",
            "Flexible use across 20 daycare days",
            "Valid for 12 months from purchase",
            "Consistent care, play & enrichment",
            "Best long-term value for regular pups",
        ],
    },
]

PLANS_TWO_DOGS = [
    {
        "name": "Double Paw Day",
        "photo": "pair-corgi-golden.webp",
        "price": "$110",
        "period": "/ 1 Day",
        "tone": PLAN_TONES["mint"],
        "features": [
            "Full day of supervised daycare",
            "$55/day per dog",
            "Safe, playful & social environment",
            "Play, enrichment & downtime",
            "Socialisation with compatible pups",
        ],
    },
    {
        "name": "Paws & Play Pack",
        "photo": "pair-samoyed-golden.webp",
        "price": "$1,000",
        "period": "/ 10 Days",
        "tone": PLAN_TONES["gold"],
        "features": [
            "10 full days of daycare",
            "$50/day per dog • Valid 6 months",
            "Consistent routine & socialisation",
            "Supervised play & enrichment",
            "Plenty of rest & relaxation",
        ],
    },
    {
        "name": "Ultimate Paw Pack",
        "photo": "pair-poodle-collie.webp",
        "price": "$1,900",
        "period": "/ 20 Days",
        "tone": PLAN_TONES["pink"],
        "features": [
            "20 full days of daycare",
            "$47.50/day per dog • Valid 12 months",
            "Best value for regular pups",
            "Daily play & enrichment",
            "Consistent care & social time",
        ],
    },
]


def services(request):
    context = {"plans_one_dog": PLANS_ONE_DOG, "plans_two_dogs": PLANS_TWO_DOGS}
    return render(request, "website/services.html", context)


def gallery(request):
    return _stub(request, "Gallery")


def contact(request):
    return _stub(request, "Contact Us")
