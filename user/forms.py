import re
from django import forms
from django.utils import timezone
from .models import Appointment, Enquiry, Service, SupportRequest


class EnquiryForm(forms.ModelForm):
    name = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(
            attrs={
                "id": "fullName",
                "class": "form-veda-control",
                "placeholder": "e.g. Ramesh Patel",
                "required": "required",
            }
        ),
        error_messages={"required": "Please provide your full name."},
    )
    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(
            attrs={
                "id": "email",
                "class": "form-veda-control",
                "placeholder": "you@example.com (optional)",
            }
        ),
        error_messages={"invalid": "Please enter a valid email address."},
    )
    phone = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.TextInput(
            attrs={
                "id": "phone",
                "class": "form-veda-control",
                "placeholder": "+91 98765 43210",
                "data-type": "indian-phone",
                "required": "required",
            }
        ),
        error_messages={"required": "Please provide your mobile number."},
    )
    city = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(
            attrs={
                "id": "city",
                "class": "form-veda-control",
                "placeholder": "e.g. Ahmedabad, Gujarat",
                "required": "required",
            }
        ),
        error_messages={"required": "Please provide your city or location."},
    )
    enquiry_type = forms.ChoiceField(
        choices=Enquiry.EnquiryType.choices,
        required=False,
        initial=Enquiry.EnquiryType.THERAPY_MACHINE,
        widget=forms.RadioSelect(
            attrs={
                "class": "enquiry-type-radio",
            }
        ),
    )
    preferred_contact_method = forms.ChoiceField(
        choices=Enquiry.ContactMethod.choices,
        required=False,
        initial=Enquiry.ContactMethod.PHONE,
        widget=forms.RadioSelect(
            attrs={
                "class": "contact-method-radio",
            }
        ),
    )
    service = forms.ModelChoiceField(
        queryset=Service.objects.none(),
        required=False,
        empty_label="-- Search for a service or product... (Optional) --",
        widget=forms.Select(
            attrs={
                "id": "serviceSelect",
                "class": "form-veda-select",
            }
        ),
    )
    usage_intention = forms.ChoiceField(
        choices=Enquiry.UsageIntention.choices,
        required=False,
        widget=forms.Select(
            attrs={
                "id": "usageIntention",
                "class": "form-veda-select",
            }
        ),
    )
    callback_time = forms.ChoiceField(
        choices=Enquiry.CallbackTime.choices,
        required=False,
        widget=forms.Select(
            attrs={
                "id": "callbackTime",
                "class": "form-veda-select",
            }
        ),
    )
    message = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                "id": "message",
                "rows": 4,
                "maxlength": 1000,
                "class": "form-veda-control",
                "placeholder": "Please describe any specific pain symptoms, questions regarding dimensions, or request for customized advice...",
            }
        ),
    )

    class Meta:
        model = Enquiry
        fields = [
            "name",
            "phone",
            "email",
            "city",
            "enquiry_type",
            "service",
            "usage_intention",
            "callback_time",
            "preferred_contact_method",
            "message",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only populate active services belonging to active categories
        self.fields["service"].queryset = (
            Service.objects.filter(is_active=True, category__is_active=True)
            .select_related("category")
            .order_by("category__name", "display_order", "name")
        )

    def clean_name(self):
        name = self.cleaned_data.get("name", "").strip()
        if not name:
            raise forms.ValidationError("Please provide your full name.")
        if len(name) < 2:
            raise forms.ValidationError("Full name must be at least 2 characters long.")
        return name

    def clean_city(self):
        city = self.cleaned_data.get("city", "").strip()
        if not city:
            raise forms.ValidationError("Please provide your city or location.")
        return city

    def clean_phone(self):
        phone_raw = self.cleaned_data.get("phone", "").strip()
        cleaned = re.sub(r"[\s\-\+\(\)]", "", phone_raw)
        if cleaned.startswith("91") and len(cleaned) == 12:
            cleaned = cleaned[2:]
        elif cleaned.startswith("0") and len(cleaned) == 11:
            cleaned = cleaned[1:]

        if not (len(cleaned) == 10 and cleaned.isdigit() and cleaned[0] in "6789"):
            raise forms.ValidationError(
                "Please enter a valid 10-digit Indian mobile number (e.g. 98250 12345)."
            )
        return cleaned

    def clean_service(self):
        service = self.cleaned_data.get("service")
        if service:
            if not service.is_active or not service.category.is_active:
                raise forms.ValidationError(
                    "The selected therapy solution is currently unavailable for enquiries."
                )
        return service


class AppointmentForm(forms.ModelForm):
    name = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(
            attrs={
                "id": "aptFullName",
                "class": "form-veda-control",
                "placeholder": "e.g. Ramesh Patel",
                "required": "required",
            }
        ),
        error_messages={"required": "Please provide your full name."},
    )
    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(
            attrs={
                "id": "aptEmail",
                "class": "form-veda-control",
                "placeholder": "you@example.com (optional)",
            }
        ),
        error_messages={"invalid": "Please enter a valid email address."},
    )
    phone = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.TextInput(
            attrs={
                "id": "aptPhone",
                "class": "form-veda-control",
                "placeholder": "+91 98765 43210",
                "data-type": "indian-phone",
                "required": "required",
            }
        ),
        error_messages={"required": "Please provide your mobile number."},
    )
    city = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(
            attrs={
                "id": "aptCity",
                "class": "form-veda-control",
                "placeholder": "e.g. Ahmedabad, Gujarat",
                "required": "required",
            }
        ),
        error_messages={"required": "Please provide your city or location."},
    )
    service = forms.ModelChoiceField(
        queryset=Service.objects.none(),
        required=True,
        empty_label="-- Select Therapy Machine / Solution * --",
        widget=forms.Select(
            attrs={
                "id": "aptService",
                "class": "form-veda-select",
                "required": "required",
            }
        ),
        error_messages={"required": "Please select a therapy machine or service of interest."},
    )
    appointment_date = forms.DateField(
        required=True,
        widget=forms.DateInput(
            attrs={
                "id": "aptDate",
                "type": "date",
                "class": "form-veda-control",
                "required": "required",
            }
        ),
        error_messages={"required": "Please select your preferred appointment date."},
    )
    time_slot = forms.ChoiceField(
        choices=Appointment.TimeSlot.choices,
        required=True,
        widget=forms.Select(
            attrs={
                "id": "aptTimeSlot",
                "class": "form-veda-select",
                "required": "required",
            }
        ),
        error_messages={"required": "Please select your preferred time slot."},
    )
    demo_format = forms.ChoiceField(
        choices=Appointment.DemoFormat.choices,
        required=False,
        initial=Appointment.DemoFormat.CENTRE,
        widget=forms.Select(
            attrs={
                "id": "aptDemoFormat",
                "class": "form-veda-select",
            }
        ),
    )
    notes = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                "id": "aptNotes",
                "rows": 3,
                "maxlength": 1000,
                "class": "form-veda-control",
                "placeholder": "Doorstep address (if Home Demo), specific knee/back discomfort, or time preferences...",
            }
        ),
    )

    class Meta:
        model = Appointment
        fields = [
            "name",
            "phone",
            "email",
            "city",
            "service",
            "appointment_date",
            "time_slot",
            "demo_format",
            "notes",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only populate active services belonging to active categories
        self.fields["service"].queryset = (
            Service.objects.filter(is_active=True, category__is_active=True)
            .select_related("category")
            .order_by("category__name", "display_order", "name")
        )

    def clean_name(self):
        name = self.cleaned_data.get("name", "").strip()
        if not name:
            raise forms.ValidationError("Please provide your full name.")
        if len(name) < 2:
            raise forms.ValidationError("Full name must be at least 2 characters long.")
        return name

    def clean_city(self):
        city = self.cleaned_data.get("city", "").strip()
        if not city:
            raise forms.ValidationError("Please provide your city or location.")
        return city

    def clean_phone(self):
        phone_raw = self.cleaned_data.get("phone", "").strip()
        cleaned = re.sub(r"[\s\-\+\(\)]", "", phone_raw)
        if cleaned.startswith("91") and len(cleaned) == 12:
            cleaned = cleaned[2:]
        elif cleaned.startswith("0") and len(cleaned) == 11:
            cleaned = cleaned[1:]

        if not (len(cleaned) == 10 and cleaned.isdigit() and cleaned[0] in "6789"):
            raise forms.ValidationError(
                "Please enter a valid 10-digit Indian mobile number (e.g. 98250 12345)."
            )
        return cleaned

    def clean_appointment_date(self):
        date = self.cleaned_data.get("appointment_date")
        if date and date < timezone.localdate():
            raise forms.ValidationError("Preferred appointment date cannot be in the past.")
        return date

    def clean_service(self):
        service = self.cleaned_data.get("service")
        if not service:
            raise forms.ValidationError("Please select a therapy machine or service of interest.")
        if not service.is_active or not service.category.is_active:
            raise forms.ValidationError(
                "The selected therapy solution is currently unavailable for appointment bookings."
            )
        return service


CONTACT_SUBJECT_CHOICES = [
    ("", "-- Choose Subject --"),
    ("Product Enquiry", "Product Specification Enquiry"),
    ("Demo Request", "Request In-Person Demo"),
    ("Clinic Setup", "Clinic / Bulk Purchase Setup"),
    ("Support", "Warranty & Support Request"),
    ("Other", "Other Feedback"),
]

PRODUCT_CHOICES = [
    ("", "-- Choose Product --"),
    ("AyurSpine Belt", "AyurSpine Lumbar Belt"),
    ("Kansa Vataki", "Kansa Vataki Foot Massager"),
    ("OrthoRelief Guard", "OrthoRelief Knee Guard"),
    ("Shirodhara Console", "Shirodhara Console"),
    ("Other", "Other Device"),
]


def _clean_indian_mobile(phone_raw):
    cleaned = re.sub(r"[\s\-\+\(\)]", "", phone_raw or "")
    if cleaned.startswith("91") and len(cleaned) == 12:
        cleaned = cleaned[2:]
    elif cleaned.startswith("0") and len(cleaned) == 11:
        cleaned = cleaned[1:]

    if not (len(cleaned) == 10 and cleaned.isdigit() and cleaned[0] in "6789"):
        raise forms.ValidationError(
            "Please enter a valid 10-digit Indian mobile number (e.g. 98250 12345)."
        )
    return cleaned


class ContactForm(forms.ModelForm):
    name = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(
            attrs={
                "id": "contactName",
                "class": "form-veda-control",
                "placeholder": "e.g. Smt. Gita Mehta",
                "required": "required",
            }
        ),
        error_messages={"required": "Please provide your full name."},
    )
    email = forms.EmailField(
        max_length=254,
        required=True,
        widget=forms.EmailInput(
            attrs={
                "id": "contactEmail",
                "class": "form-veda-control",
                "placeholder": "gita@example.com",
                "required": "required",
            }
        ),
        error_messages={
            "required": "Please provide your email address.",
            "invalid": "Please enter a valid email address.",
        },
    )
    phone = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.TextInput(
            attrs={
                "id": "contactPhone",
                "class": "form-veda-control",
                "data-type": "indian-phone",
                "placeholder": "98250 12345",
                "required": "required",
            }
        ),
        error_messages={"required": "Please provide your mobile number."},
    )
    subject = forms.ChoiceField(
        choices=CONTACT_SUBJECT_CHOICES,
        required=True,
        widget=forms.Select(
            attrs={
                "id": "contactSubject",
                "class": "form-veda-select",
                "required": "required",
            }
        ),
        error_messages={"required": "Please select a subject."},
    )
    message = forms.CharField(
        required=True,
        widget=forms.Textarea(
            attrs={
                "id": "contactMessage",
                "rows": 4,
                "class": "form-veda-control",
                "placeholder": "Write your questions or notes here...",
                "required": "required",
            }
        ),
        error_messages={"required": "Please provide your message details."},
    )

    class Meta:
        model = SupportRequest
        fields = ["name", "email", "phone", "subject", "message"]

    def clean_name(self):
        name = self.cleaned_data.get("name", "").strip()
        if not name:
            raise forms.ValidationError("Please provide your full name.")
        if len(name) < 2:
            raise forms.ValidationError("Full name must be at least 2 characters long.")
        return name

    def clean_phone(self):
        return _clean_indian_mobile(self.cleaned_data.get("phone", "").strip())

    def clean_message(self):
        msg = self.cleaned_data.get("message", "").strip()
        if not msg:
            raise forms.ValidationError("Please provide your message details.")
        if len(msg) < 5:
            raise forms.ValidationError("Message must be at least 5 characters long.")
        return msg

    def save(self, commit=True):
        instance = super().save(commit=False)
        subj = self.cleaned_data.get("subject", "")
        if subj == "Demo Request":
            instance.request_type = SupportRequest.RequestType.DEMO_REQUEST
        elif subj == "Clinic Setup":
            instance.request_type = SupportRequest.RequestType.CLINIC_SETUP
        elif subj == "Support":
            instance.request_type = SupportRequest.RequestType.PRODUCT_SUPPORT
        elif subj == "Other":
            instance.request_type = SupportRequest.RequestType.FEEDBACK
        else:
            instance.request_type = SupportRequest.RequestType.CONTACT
        instance.status = SupportRequest.Status.NEW
        if commit:
            instance.save()
        return instance


class SupportTicketForm(forms.ModelForm):
    name = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(
            attrs={
                "id": "supName",
                "class": "form-veda-control",
                "placeholder": "Rakesh Vora",
                "required": "required",
            }
        ),
        error_messages={"required": "Please provide your full name."},
    )
    email = forms.EmailField(
        max_length=254,
        required=True,
        widget=forms.EmailInput(
            attrs={
                "id": "supEmail",
                "class": "form-veda-control",
                "placeholder": "rakesh@example.com",
                "required": "required",
            }
        ),
        error_messages={
            "required": "Please provide your email address.",
            "invalid": "Please enter a valid email address.",
        },
    )
    phone = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.TextInput(
            attrs={
                "id": "supPhone",
                "class": "form-veda-control",
                "data-type": "indian-phone",
                "placeholder": "98250 12345",
                "required": "required",
            }
        ),
        error_messages={"required": "Please provide your mobile phone number."},
    )
    product_name = forms.ChoiceField(
        choices=PRODUCT_CHOICES,
        required=True,
        widget=forms.Select(
            attrs={
                "id": "supProduct",
                "class": "form-veda-select",
                "required": "required",
            }
        ),
        error_messages={"required": "Please select equipment."},
    )
    message = forms.CharField(
        required=True,
        widget=forms.Textarea(
            attrs={
                "id": "supDesc",
                "rows": 4,
                "class": "form-veda-control",
                "placeholder": "Describe what part requires replacement or guidance...",
                "required": "required",
            }
        ),
        error_messages={"required": "Please describe the issue."},
    )

    class Meta:
        model = SupportRequest
        fields = ["name", "email", "phone", "product_name", "message"]

    def clean_name(self):
        name = self.cleaned_data.get("name", "").strip()
        if not name:
            raise forms.ValidationError("Please provide your full name.")
        if len(name) < 2:
            raise forms.ValidationError("Full name must be at least 2 characters long.")
        return name

    def clean_phone(self):
        return _clean_indian_mobile(self.cleaned_data.get("phone", "").strip())

    def clean_message(self):
        msg = self.cleaned_data.get("message", "").strip()
        if not msg:
            raise forms.ValidationError("Please describe the issue.")
        if len(msg) < 5:
            raise forms.ValidationError("Issue description must be at least 5 characters long.")
        return msg

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.request_type = SupportRequest.RequestType.PRODUCT_SUPPORT
        prod = self.cleaned_data.get("product_name", "")
        instance.subject = f"Support: {prod}" if prod else "Product Support"
        instance.status = SupportRequest.Status.NEW
        if commit:
            instance.save()
        return instance


