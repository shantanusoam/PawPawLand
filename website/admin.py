from django.contrib import admin

from .models import FAQ, GalleryImage, Service, Testimonial


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
