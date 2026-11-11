from django.db import migrations


INSTAGRAM_URL = "https://www.instagram.com/pawpawland.blackburn/"
FACEBOOK_URL = "https://www.facebook.com/people/Pawpaw-Land/61573433516046/"


def set_social_links(apps, schema_editor):
    SiteSettings = apps.get_model("website", "SiteSettings")
    obj, _ = SiteSettings.objects.get_or_create(pk=1)
    if not obj.instagram_url:
        obj.instagram_url = INSTAGRAM_URL
    if not obj.facebook_url:
        obj.facebook_url = FACEBOOK_URL
    obj.save()


def unset_social_links(apps, schema_editor):
    SiteSettings = apps.get_model("website", "SiteSettings")
    obj, _ = SiteSettings.objects.get_or_create(pk=1)
    if obj.instagram_url == INSTAGRAM_URL:
        obj.instagram_url = ""
    if obj.facebook_url == FACEBOOK_URL:
        obj.facebook_url = ""
    obj.save()


class Migration(migrations.Migration):

    dependencies = [
        ("website", "0014_registration_heard_about_and_more"),
    ]

    operations = [
        migrations.RunPython(set_social_links, unset_social_links),
    ]
