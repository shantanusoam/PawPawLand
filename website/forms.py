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


_RADIO_CLASSES = "flex items-center gap-2 text-sm text-ink"
_DATE_CLASSES = _INPUT_CLASSES + " [color-scheme:light]"
_FILE_CLASSES = (
    "block w-full rounded-lg border border-navy/15 bg-[#fafafa] px-4 py-3 text-sm text-ink "
    "file:mr-3 file:rounded file:border-0 file:bg-navy/10 file:px-3 file:py-1.5 "
    "file:text-sm file:font-semibold file:text-navy"
)


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Registration
        fields = [
            "owner_name",
            "address",
            "suburb",
            "postcode",
            "phone",
            "email",
            "emergency_contact_name",
            "emergency_contact_phone",
            "vet_clinic_name",
            "vet_phone",
            "dog_name",
            "microchip_number",
            "dog_photo",
            "breed",
            "colour",
            "date_of_birth",
            "gender",
            "is_desexed",
            "has_aggression",
            "aggression_details",
            "last_vaccination_date",
            "vaccination_certificate",
            "has_health_ailments",
            "health_ailments_details",
            "has_medication",
            "medication_details",
            "food_allergies",
            "instagram_handle",
            "agreed_to_terms",
        ]
        widgets = {
            "owner_name": forms.TextInput(
                attrs={"class": _INPUT_CLASSES, "placeholder": "Jamie Smith"}
            ),
            "address": forms.TextInput(
                attrs={"class": _INPUT_CLASSES, "placeholder": "123 Example Street"}
            ),
            "suburb": forms.TextInput(attrs={"class": _INPUT_CLASSES, "placeholder": "Blackburn"}),
            "postcode": forms.TextInput(attrs={"class": _INPUT_CLASSES, "placeholder": "3130"}),
            "phone": forms.TextInput(
                attrs={"class": _INPUT_CLASSES, "placeholder": "04XX XXX XXX"}
            ),
            "email": forms.EmailInput(
                attrs={"class": _INPUT_CLASSES, "placeholder": "jamie@example.com"}
            ),
            "emergency_contact_name": forms.TextInput(
                attrs={"class": _INPUT_CLASSES, "placeholder": "Jamie Smith"}
            ),
            "emergency_contact_phone": forms.TextInput(
                attrs={"class": _INPUT_CLASSES, "placeholder": "04XX XXX XXX"}
            ),
            "vet_clinic_name": forms.TextInput(
                attrs={"class": _INPUT_CLASSES, "placeholder": "Blackburn Vet Clinic"}
            ),
            "vet_phone": forms.TextInput(
                attrs={"class": _INPUT_CLASSES, "placeholder": "04XX XXX XXX"}
            ),
            "dog_name": forms.TextInput(attrs={"class": _INPUT_CLASSES, "placeholder": "Biscuit"}),
            "microchip_number": forms.TextInput(attrs={"class": _INPUT_CLASSES}),
            "dog_photo": forms.ClearableFileInput(attrs={"class": _FILE_CLASSES}),
            "breed": forms.TextInput(
                attrs={"class": _INPUT_CLASSES, "placeholder": "Golden Retriever"}
            ),
            "colour": forms.TextInput(attrs={"class": _INPUT_CLASSES, "placeholder": "Golden"}),
            "date_of_birth": forms.DateInput(
                attrs={"class": _DATE_CLASSES, "type": "date"}, format="%Y-%m-%d"
            ),
            "gender": forms.RadioSelect(attrs={"class": _RADIO_CLASSES}),
            "is_desexed": forms.RadioSelect(attrs={"class": _RADIO_CLASSES}),
            "has_aggression": forms.RadioSelect(attrs={"class": _RADIO_CLASSES}),
            "aggression_details": forms.Textarea(
                attrs={
                    "class": _INPUT_CLASSES,
                    "rows": 3,
                    "placeholder": "Please give us more detail...",
                }
            ),
            "last_vaccination_date": forms.DateInput(
                attrs={"class": _DATE_CLASSES, "type": "date"}, format="%Y-%m-%d"
            ),
            "vaccination_certificate": forms.ClearableFileInput(attrs={"class": _FILE_CLASSES}),
            "has_health_ailments": forms.RadioSelect(attrs={"class": _RADIO_CLASSES}),
            "health_ailments_details": forms.Textarea(
                attrs={
                    "class": _INPUT_CLASSES,
                    "rows": 3,
                    "placeholder": "Please give us more detail...",
                }
            ),
            "has_medication": forms.RadioSelect(attrs={"class": _RADIO_CLASSES}),
            "medication_details": forms.Textarea(
                attrs={
                    "class": _INPUT_CLASSES,
                    "rows": 3,
                    "placeholder": "Please give us more detail...",
                }
            ),
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
            "agreed_to_terms": forms.CheckboxInput(attrs={"class": "h-4 w-4"}),
        }
        labels = {
            "owner_name": "Owner's Name",
            "address": "Address",
            "suburb": "Suburb",
            "postcode": "Postcode",
            "phone": "Phone",
            "email": "Email Address",
            "emergency_contact_name": "Name",
            "emergency_contact_phone": "Phone",
            "vet_clinic_name": "Vet Clinic Name",
            "vet_phone": "Phone",
            "dog_name": "Name of Dog",
            "microchip_number": "Microchip Number",
            "dog_photo": "Dog Photo *",
            "breed": "Breed",
            "colour": "Colour",
            "date_of_birth": "Date of Birth",
            "gender": "Gender",
            "is_desexed": "Is your dog desexed?",
            "has_aggression": "Does your dog display aggression to other dogs or people?",
            "aggression_details": "If yes, please specify",
            "last_vaccination_date": "Last Vaccination Date *",
            "vaccination_certificate": "Vaccination Certificate *",
            "has_health_ailments": "Does your dog suffer from any health issues?",
            "health_ailments_details": "If yes, please specify",
            "has_medication": "Is your dog on any medication?",
            "medication_details": "If yes, please specify",
            "food_allergies": "Does your dog have any food allergies or dietary sensitivities "
            "we should know about?",
            "instagram_handle": "We share daycare updates on our Instagram Stories. If you're "
            "happy for us to tag your pup, please share their Instagram handle below (optional).",
            "agreed_to_terms": "I agree with the Terms & Conditions",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["food_allergies"].required = False
        self.fields["instagram_handle"].required = False
        self.fields["aggression_details"].required = False
        self.fields["health_ailments_details"].required = False
        self.fields["medication_details"].required = False

    def clean_agreed_to_terms(self):
        agreed = self.cleaned_data.get("agreed_to_terms")
        if not agreed:
            raise forms.ValidationError("You must agree to the Terms & Conditions to register.")
        return agreed
