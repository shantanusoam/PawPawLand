from django import forms

from .models import ContactSubmission

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
