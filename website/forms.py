from django import forms

from .models import ContactSubmission, Registration

_INPUT_CLASSES = (
    "w-full rounded-lg border border-navy/15 bg-[#fafafa] px-4 py-3 text-sm text-ink "
    "placeholder:text-ink/40 focus:border-navy focus:ring-1 focus:ring-navy focus:outline-none"
)


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactSubmission
        fields = ["full_name", "email", "phone", "service_requested", "message"]
        widgets = {
            "full_name": forms.TextInput(
                attrs={"class": _INPUT_CLASSES, "placeholder": "Jamie Smith"}
            ),
            "email": forms.EmailInput(
                attrs={"class": _INPUT_CLASSES, "placeholder": "jamie@example.com"}
            ),
            "phone": forms.TextInput(
                attrs={"class": _INPUT_CLASSES, "placeholder": "04XX XXX XXX"}
            ),
            "service_requested": forms.Select(attrs={"class": _INPUT_CLASSES}),
            "message": forms.Textarea(
                attrs={
                    "class": _INPUT_CLASSES,
                    "placeholder": "Briefly describe your requirement...",
                    "rows": 4,
                }
            ),
        }
        labels = {
            "full_name": "Full Name",
            "email": "Email Address",
            "phone": "Phone Number",
            "service_requested": "Service Required",
            "message": "Enquiry",
        }

    def __init__(self, *args, service_choices=(), **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["phone"].required = False
        self.fields["service_requested"].required = False
        self.fields["service_requested"].widget.choices = [("", "Select a service")] + list(
            service_choices
        )


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Registration
        fields = ["full_name", "email", "phone", "dog_name", "food_allergies", "instagram_handle"]
        widgets = {
            "full_name": forms.TextInput(
                attrs={"class": _INPUT_CLASSES, "placeholder": "Jamie Smith"}
            ),
            "email": forms.EmailInput(
                attrs={"class": _INPUT_CLASSES, "placeholder": "jamie@example.com"}
            ),
            "phone": forms.TextInput(
                attrs={"class": _INPUT_CLASSES, "placeholder": "04XX XXX XXX"}
            ),
            "dog_name": forms.TextInput(attrs={"class": _INPUT_CLASSES, "placeholder": "Biscuit"}),
            "food_allergies": forms.Textarea(
                attrs={
                    "class": _INPUT_CLASSES,
                    "placeholder": "Please let us know about any foods, ingredients or "
                    "treats your dog should avoid.",
                    "rows": 4,
                }
            ),
            "instagram_handle": forms.TextInput(
                attrs={"class": _INPUT_CLASSES, "placeholder": "@_____"}
            ),
        }
        labels = {
            "full_name": "Full Name",
            "email": "Email Address",
            "phone": "Phone Number",
            "dog_name": "Dog's Name",
            "food_allergies": "Does your dog have any food allergies or dietary sensitivities "
            "we should know about?",
            "instagram_handle": "We share daycare updates on our Instagram Stories. If you're "
            "happy for us to tag your pup, please share their Instagram handle below (optional).",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["phone"].required = False
        self.fields["food_allergies"].required = False
        self.fields["instagram_handle"].required = False
