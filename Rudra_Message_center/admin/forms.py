from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.text import slugify
from user.models import (
    Appointment,
    BodyPart,
    Category,
    CustomerNeed,
    Enquiry,
    IntendedUse,
    Offer,
    Service,
    ServiceType,
    SiteSettings,
    SupportRequest,
)


class AdminLoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Staff Username",
        widget=forms.TextInput(
            attrs={
                "class": "custom-input",
                "placeholder": "Enter your staff username",
                "id": "adminUsername",
                "autocomplete": "username",
                "autofocus": True,
            }
        ),
    )
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "class": "custom-input",
                "placeholder": "Enter your password",
                "id": "adminPassword",
                "autocomplete": "current-password",
            }
        ),
    )


class EnquiryStatusForm(forms.ModelForm):
    customer_response = forms.CharField(
        required=False,
        label="Message to Customer",
        help_text="If entered, this message will be emailed directly to the customer's registered email.",
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "rows": 4,
                "placeholder": "Type response to email directly to customer...",
                "id": "enquiryCustomerResponse",
            }
        ),
    )
    send_email_notification = forms.BooleanField(
        required=False,
        initial=True,
        label="Send Email Notification",
        help_text="Notify customer of this status update/response via email.",
        widget=forms.CheckboxInput(attrs={"class": "form-check-input", "role": "switch", "id": "enquirySendEmailSwitch"}),
    )

    class Meta:
        model = Enquiry
        fields = ["status", "admin_notes"]
        widgets = {
            "status": forms.Select(attrs={"class": "form-select"}),
            "admin_notes": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Enter internal follow-up notes, phone consultation details, demo interest, etc...",
                }
            ),
        }

    def clean_status(self):
        status = self.cleaned_data.get("status")
        if status not in dict(Enquiry.Status.choices):
            raise forms.ValidationError("Invalid enquiry workflow status choice.")
        return status


class AppointmentStatusForm(forms.ModelForm):
    appointment_date = forms.DateField(
        required=False,
        label="Scheduled Date",
        widget=forms.DateInput(attrs={"class": "form-control", "type": "date", "id": "appointmentDateInput"}),
    )
    time_slot = forms.ChoiceField(
        choices=Appointment.TimeSlot.choices,
        required=False,
        label="Time Slot",
        widget=forms.Select(attrs={"class": "form-select", "id": "appointmentTimeSlotSelect"}),
    )
    customer_response = forms.CharField(
        required=False,
        label="Message to Customer",
        help_text="Personalized note emailed directly to the client regarding this appointment.",
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "rows": 4,
                "placeholder": "Type message to email directly to client (e.g. confirmation instructions, rescheduling notes)...",
                "id": "appointmentCustomerResponse",
            }
        ),
    )
    send_email_notification = forms.BooleanField(
        required=False,
        initial=True,
        label="Send Email Notification",
        help_text="Send email notification to client regarding this update.",
        widget=forms.CheckboxInput(attrs={"class": "form-check-input", "role": "switch", "id": "appointmentSendEmailSwitch"}),
    )

    class Meta:
        model = Appointment
        fields = ["status", "admin_notes"]
        widgets = {
            "status": forms.Select(attrs={"class": "form-select", "id": "appointmentStatusSelect"}),
            "admin_notes": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Enter internal staff notes, demonstration location/time arrangements, client follow-up feedback...",
                    "id": "appointmentAdminNotes",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            if not self.initial.get("appointment_date") and self.instance.appointment_date:
                self.initial["appointment_date"] = self.instance.appointment_date
            if not self.initial.get("time_slot") and self.instance.time_slot:
                self.initial["time_slot"] = self.instance.time_slot

    def clean_status(self):
        status = self.cleaned_data.get("status")
        if status not in dict(Appointment.Status.choices):
            raise forms.ValidationError("Invalid appointment status choice.")
        return status

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.cleaned_data.get("appointment_date"):
            instance.appointment_date = self.cleaned_data["appointment_date"]
        if self.cleaned_data.get("time_slot"):
            instance.time_slot = self.cleaned_data["time_slot"]
        if commit:
            instance.save()
        return instance


class SupportRequestStatusForm(forms.ModelForm):
    customer_response = forms.CharField(
        required=False,
        label="Message to Customer",
        help_text="Resolution instructions or troubleshooting reply emailed to the customer.",
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "rows": 4,
                "placeholder": "Type resolution details or reply to email customer...",
                "id": "supportCustomerResponse",
            }
        ),
    )
    send_email_notification = forms.BooleanField(
        required=False,
        initial=True,
        label="Send Email Notification",
        help_text="Send email notification with resolution/update to customer.",
        widget=forms.CheckboxInput(attrs={"class": "form-check-input", "role": "switch", "id": "supportSendEmailSwitch"}),
    )

    class Meta:
        model = SupportRequest
        fields = ["status", "admin_notes"]
        widgets = {
            "status": forms.Select(attrs={"class": "form-select", "id": "supportRequestStatusSelect"}),
            "admin_notes": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Enter internal notes regarding client call, warranty review, technician follow-up...",
                    "id": "supportRequestAdminNotes",
                }
            ),
        }

    def clean_status(self):
        status = self.cleaned_data.get("status")
        if status not in dict(SupportRequest.Status.choices):
            raise forms.ValidationError("Invalid support request status choice.")
        return status


class CategoryAdminForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = [
            "name",
            "slug",
            "description",
            "image",
            "is_active",
            "display_order",
        ]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter Category name",
                }
            ),
            "slug": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter Url Slug",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Enter Category description",
                }
            ),
            "image": forms.ClearableFileInput(
                attrs={
                    "class": "form-control",
                    "accept": "image/*",
                }
            ),
            "is_active": forms.CheckboxInput(
                attrs={"class": "form-check-input", "role": "switch"}
            ),
            "display_order": forms.NumberInput(
                attrs={"class": "form-control", "style": "max-width: 140px;"}
            ),
        }

    def clean_name(self):
        name = self.cleaned_data.get("name", "").strip()
        if not name:
            raise forms.ValidationError("Category name cannot be only whitespace.")
        # Check uniqueness excluding current instance
        qs = Category.objects.filter(name__iexact=name)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("A category with this name already exists.")
        return name

    def clean_slug(self):
        slug = self.cleaned_data.get("slug", "").strip()
        if not slug:
            name = self.cleaned_data.get("name", "").strip()
            slug = slugify(name)
        else:
            slug = slugify(slug)

        qs = Category.objects.filter(slug=slug)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("A category with this slug already exists.")
        return slug


class ServiceAdminForm(forms.ModelForm):
    customer_needs = forms.ModelMultipleChoiceField(
        queryset=CustomerNeed.objects.filter(is_active=True).order_by("name"),
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={"class": "form-check-input"}),
        help_text="Target ailments or customer benefits",
    )
    body_parts = forms.ModelMultipleChoiceField(
        queryset=BodyPart.objects.filter(is_active=True).order_by("name"),
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={"class": "form-check-input"}),
        help_text="Anatomical areas addressed",
    )
    service_types = forms.ModelMultipleChoiceField(
        queryset=ServiceType.objects.filter(is_active=True).order_by("name"),
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={"class": "form-check-input"}),
        help_text="Product or therapy modality classifications",
    )
    intended_uses = forms.ModelMultipleChoiceField(
        queryset=IntendedUse.objects.filter(is_active=True).order_by("name"),
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={"class": "form-check-input"}),
        help_text="Recommended settings (Home, Clinic, Senior Care, etc.)",
    )

    class Meta:
        model = Service
        fields = [
            "name",
            "slug",
            "category",
            "short_description",
            "description",
            "image",
            "benefits",
            "usage_instructions",
            "precautions",
            "is_featured",
            "is_active",
            "display_order",
            "customer_needs",
            "body_parts",
            "service_types",
            "intended_uses",
        ]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter Product name",
                }
            ),
            "slug": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter Url Slug",
                }
            ),
            "category": forms.Select(attrs={"class": "form-select"}),
            "short_description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 2,
                    "placeholder": "describe machine",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 5,
                    "placeholder": "Enter Full description",
                }
            ),
            "image": forms.ClearableFileInput(
                attrs={
                    "class": "form-control",
                    "accept": "image/*",
                }
            ),
            "benefits": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Enter therapeutic benefits",
                }
            ),
            "usage_instructions": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Enter usage instructions",
                }
            ),
            "precautions": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Enter precautions or warnings",
                }
            ),
            "is_featured": forms.CheckboxInput(
                attrs={"class": "form-check-input", "role": "switch"}
            ),
            "is_active": forms.CheckboxInput(
                attrs={"class": "form-check-input", "role": "switch"}
            ),
            "display_order": forms.NumberInput(
                attrs={"class": "form-control", "style": "max-width: 140px;"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Populate all categories, prioritizing active ones
        self.fields["category"].queryset = Category.objects.all().order_by(
            "-is_active", "display_order", "name"
        )
        self.fields["category"].empty_label = "-- Select Category --"

    def clean_name(self):
        name = self.cleaned_data.get("name", "").strip()
        if not name:
            raise forms.ValidationError("Service name cannot be only whitespace.")
        return name

    def clean_short_description(self):
        short_description = self.cleaned_data.get("short_description", "").strip()
        if not short_description:
            raise forms.ValidationError("Short description cannot be only whitespace.")
        return short_description

    def clean_slug(self):
        slug = self.cleaned_data.get("slug", "").strip()
        if not slug:
            name = self.cleaned_data.get("name", "").strip()
            slug = slugify(name)
        else:
            slug = slugify(slug)

        qs = Service.objects.filter(slug=slug)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("A product/service with this slug already exists.")
        return slug


class SiteSettingsForm(forms.ModelForm):
    class Meta:
        model = SiteSettings
        fields = [
            "business_name",
            "primary_phone",
            "contact_email",
            "whatsapp_number",
            "business_address",
            "google_maps_url",
            "business_hours",
            "enable_announcement_banner",
            "enable_whatsapp_floating",
        ]
        widgets = {
            "business_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "id": "settingsDisplayName",
                    "placeholder": "e.g. Rudra Massage & Wellness",
                }
            ),
            "primary_phone": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "id": "settingsPhone",
                    "placeholder": "e.g. +91 98250 00000",
                }
            ),
            "contact_email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "id": "settingsEmail",
                    "placeholder": "e.g. care@rudrawellness.com",
                }
            ),
            "whatsapp_number": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "id": "settingsWhatsApp",
                    "placeholder": "e.g. +91 98250 00000",
                }
            ),
            "business_address": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "id": "settingsAddress",
                    "placeholder": "Full physical experience centre address...",
                }
            ),
            "google_maps_url": forms.URLInput(
                attrs={
                    "class": "form-control",
                    "id": "settingsMapsUrl",
                    "placeholder": "https://maps.google.com/...",
                }
            ),
            "business_hours": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "id": "settingsHours",
                    "placeholder": "e.g. Mon - Sat: 9:30 AM - 7:00 PM | Sun: By Appointment",
                }
            ),
            "enable_announcement_banner": forms.CheckboxInput(
                attrs={"class": "form-check-input", "role": "switch", "id": "announcementToggle"}
            ),
            "enable_whatsapp_floating": forms.CheckboxInput(
                attrs={"class": "form-check-input", "role": "switch", "id": "whatsappFloatingToggle"}
            ),
        }
        error_messages = {
            "business_name": {"required": "Business name cannot be only whitespace."},
            "primary_phone": {"required": "Primary phone cannot be only whitespace."},
            "contact_email": {
                "required": "Contact email cannot be only whitespace.",
                "invalid": "Enter a valid email address.",
            },
            "business_address": {"required": "Business address cannot be only whitespace."},
        }

    def clean_business_name(self):
        name = self.cleaned_data.get("business_name", "").strip()
        if not name:
            raise forms.ValidationError("Business name cannot be only whitespace.")
        return name

    def clean_primary_phone(self):
        phone = self.cleaned_data.get("primary_phone", "").strip()
        if not phone:
            raise forms.ValidationError("Primary phone cannot be only whitespace.")
        return phone

    def clean_contact_email(self):
        email = self.cleaned_data.get("contact_email", "").strip()
        if not email:
            raise forms.ValidationError("Contact email cannot be only whitespace.")
        return email

    def clean_business_address(self):
        addr = self.cleaned_data.get("business_address", "").strip()
        if not addr:
            raise forms.ValidationError("Business address cannot be only whitespace.")
        return addr

