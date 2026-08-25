from django.contrib import admin
from django.shortcuts import redirect
from django.urls import reverse

from .models import (
    FAQ,
    ContactSubmission,
    GalleryImage,
    PricingPlan,
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


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ["author_name", "dog_name", "rating", "sort_order", "is_active"]
    list_editable = ["sort_order", "is_active"]


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ["question", "sort_order", "is_active"]
    list_editable = ["sort_order", "is_active"]


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ["alt_text", "row", "sort_order", "is_active"]
    list_editable = ["row", "sort_order", "is_active"]


@admin.register(PricingPlan)
class PricingPlanAdmin(admin.ModelAdmin):
    list_display = ["name", "dog_count", "price", "period_label", "tone", "sort_order", "is_active"]
    list_editable = ["sort_order", "is_active"]
    list_filter = ["dog_count", "tone"]


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
