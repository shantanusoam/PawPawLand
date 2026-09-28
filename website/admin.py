from django.contrib import admin
from django.shortcuts import redirect
from django.urls import reverse

from .models import (
    FAQ,
    ContactSubmission,
    GalleryImage,
    LegalPage,
    PricingPlan,
    Registration,
    Service,
    SiteSettings,
    TeamMember,
    Testimonial,
)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ["name", "price_label", "sort_order", "is_active"]
    list_editable = ["sort_order", "is_active"]
    prepopulated_fields = {"slug": ["name"]}
    fieldsets = [
        (
            None,
            {
                "fields": [
                    "name",
                    "slug",
                    "emoji_badge",
                    "image",
                    "description",
                    "price_label",
                    "sort_order",
                    "is_active",
                ]
            },
        ),
        (
            "Pricing plan headings (optional)",
            {
                "classes": ["collapse"],
                "description": "Leave blank to use the site's default pricing headings.",
                "fields": [
                    "tagline_1dog_plain",
                    "tagline_1dog_gold",
                    "tagline_2dogs_plain",
                    "tagline_2dogs_gold",
                    "tagline_3dogs_plain",
                    "tagline_3dogs_gold",
                ],
            },
        ),
    ]


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ["author_name", "dog_name", "rating", "sort_order", "is_active"]
    list_editable = ["sort_order", "is_active"]


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ["question", "sort_order", "is_active"]
    list_editable = ["sort_order", "is_active"]


@admin.register(LegalPage)
class LegalPageAdmin(admin.ModelAdmin):
    list_display = ["title", "slug"]
    prepopulated_fields = {"slug": ["title"]}


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ["alt_text", "service", "row", "sort_order", "is_active"]
    list_editable = ["row", "sort_order", "is_active"]
    list_filter = ["service", "row"]


@admin.register(PricingPlan)
class PricingPlanAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "service",
        "dog_count",
        "price",
        "period_label",
        "price_tiers_badge",
        "tone",
        "sort_order",
        "is_active",
    ]
    list_editable = ["sort_order", "is_active"]
    list_filter = ["service", "dog_count", "tone"]

    @admin.display(description="Prices")
    def price_tiers_badge(self, obj):
        if obj.is_triple_price:
            return "3"
        if obj.is_dual_price:
            return "2"
        return "1"

    fieldsets = [
        (None, {"fields": ["name", "service", "dog_count", "photo", "tone", "features_text"]}),
        (
            "Price 1",
            {"fields": ["price", "period_label", "price_caption"]},
        ),
        (
            "Price 2 (optional — leave blank for a single-price card)",
            {"fields": ["price_2", "period_label_2", "price_2_caption"]},
        ),
        (
            "Price 3 (optional — only used when Price 2 is also set)",
            {"fields": ["price_3", "period_label_3", "price_3_caption"]},
        ),
        ("Visibility", {"fields": ["sort_order", "is_active"]}),
    ]


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ["name", "role", "sort_order", "is_active"]
    list_editable = ["sort_order", "is_active"]


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        # Singleton: skip the list page and go straight to the one editable row.
        SiteSettings.load()
        return redirect(reverse("admin:website_sitesettings_change", args=[1]))


@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ["full_name", "email", "service_requested", "created_at", "is_read"]
    list_editable = ["is_read"]
    list_filter = ["is_read", "service_requested"]
    search_fields = ["full_name", "email", "message"]
    readonly_fields = ["full_name", "email", "phone", "service_requested", "message", "created_at"]

    def has_add_permission(self, request):
        return False


@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ["dog_name", "full_name", "email", "created_at", "is_read"]
    list_editable = ["is_read"]
    list_filter = ["is_read"]
    search_fields = ["dog_name", "full_name", "email"]
    readonly_fields = [
        "full_name",
        "email",
        "phone",
        "dog_name",
        "food_allergies",
        "instagram_handle",
        "created_at",
    ]

    def has_add_permission(self, request):
        return False
