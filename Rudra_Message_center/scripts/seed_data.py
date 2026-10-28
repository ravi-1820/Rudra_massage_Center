#!/usr/bin/env python
"""
Seed script for Rudra Massage & Wellness.

Seeds the administrative superuser credentials and the 5 core existing
equipment/service records along with their respective categories and taxonomies.
Uses transaction safety and comprehensive exception handling.
"""

import os
import sys
from pathlib import Path

# Add project root to Python path and setup Django
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rudra_massage_center.settings")

try:
    import django
    django.setup()
    from django.contrib.auth import get_user_model
    from django.db import transaction, DatabaseError
    from user.models import (
        Category,
        Service,
        CustomerNeed,
        BodyPart,
        ServiceType,
        IntendedUse,
        SiteSettings,
    )
except ImportError as err:
    print(f"Error: Unable to import Django or project modules: {err}")
    sys.exit(1)


# ---------------------------------------------------------
# Seed Data Definitions (Exact 5 Existing Core Products)
# ---------------------------------------------------------
ADMIN_CREDENTIALS = {
    "username": os.getenv("ADMIN_USERNAME", "admin"),
    "email": os.getenv("ADMIN_EMAIL", "admin@gmail.com"),
    "password": os.getenv("ADMIN_PASSWORD", "admin"),
}

EXISTING_SERVICES_DATA = [
    {
        "category": {
            "name": "Back Massage & Therapy Equipment",
            "slug": "back-massage-therapy-equipment",
            "description": "",
            "display_order": 1,
            "is_active": True,
        },
        "service": {
            "name": "Back Pain Machine",
            "slug": "back-pain-machine",
            "short_description": "A back-focused wellness device. Please refer to the verified product specifications and manufacturer instructions for its intended use and features.",
            "description": (
                "Explore the Back Pain Machine available in the Rudra Massage & Wellness catalogue.\n\n"
                "The product page should include the verified operating method, available settings, equipment specifications, "
                "intended use and maintenance instructions for the actual model.\n\n"
                "Contact our team for product information, availability and usage documentation."
            ),
            "benefits": (
                "• Intended purpose depends on the specific device and its manufacturer documentation.\n"
                "• Product features and appropriate uses should be confirmed before purchase."
            ),
            "usage_instructions": (
                "• Read the manufacturer's instruction manual before use.\n"
                "• Operate the device only as specified by the manufacturer.\n"
                "• Follow the recommended cleaning and maintenance instructions."
            ),
            "precautions": (
                "• Do not use the device as a substitute for medical assessment or treatment.\n"
                "• Follow all manufacturer warnings and contraindications.\n"
                "• Seek appropriate professional guidance if back pain is persistent or unexplained."
            ),
            "is_featured": True,
            "is_active": True,
            "display_order": 1,
            "customer_needs": ["Back Pain"],
            "body_parts": ["Back"],
            "service_types": ["Massagers", "Therapy Machines"],
            "intended_uses": ["Clinic/Centre"],
        },
    },
    {
        "category": {
            "name": "Body Composition & BMI Equipment",
            "slug": "body-composition-bmi-equipment",
            "description": "",
            "display_order": 2,
            "is_active": True,
        },
        "service": {
            "name": "Body Mass Index (BMI)",
            "slug": "body-mass-index-bmi",
            "short_description": "A body measurement or BMI-related product. Confirm whether the item measures body composition, calculates BMI, or provides another type of health measurement.",
            "description": (
                "Explore the BMI-related equipment listed in the Rudra Massage & Wellness catalogue.\n\n"
                "The product's exact measurement capabilities, operating method, display features and technical specifications "
                "should be confirmed from the actual model's documentation.\n\n"
                "BMI is a screening measure calculated from height and weight. It is not, by itself, a diagnosis or a complete assessment of health."
            ),
            "benefits": (
                "• May support basic health measurement or wellness tracking, depending on the actual device.\n"
                "• Measurement capabilities must be confirmed from the manufacturer documentation."
            ),
            "usage_instructions": (
                "• Follow the instructions supplied with the actual device.\n"
                "• Enter or measure the required information correctly.\n"
                "• Follow the manufacturer's guidance for interpreting displayed results."
            ),
            "precautions": (
                "• Do not use BMI alone to diagnose a health condition.\n"
                "• Measurement accuracy depends on the device and method used.\n"
                "• Seek qualified professional advice when interpreting health measurements."
            ),
            "is_featured": True,
            "is_active": True,
            "display_order": 2,
            "customer_needs": ["Weight Management"],
            "body_parts": [],
            "service_types": ["Exercise Equipment"],
            "intended_uses": ["Clinic/Centre"],
        },
    },
    {
        "category": {
            "name": "Traditional Wellness Equipment",
            "slug": "traditional-wellness-equipment",
            "description": "",
            "display_order": 8,
            "is_active": True,
        },
        "service": {
            "name": "Eagle Health Mate",
            "slug": "eagle-health-mate",
            "short_description": "Explore Eagle Health Mate wellness equipment. Contact Rudra Massage & Wellness to confirm its functions, specifications and intended use.",
            "description": (
                "Eagle Health Mate is listed in the Rudra Massage & Wellness product inventory.\n\n"
                "The exact model and operating principle need to be verified before publishing detailed technical information. "
                "Add manufacturer-confirmed specifications, intended use, operating instructions and maintenance information to this page.\n\n"
                "Contact our team for product details and availability."
            ),
            "benefits": (
                "• Product-specific benefits have not yet been verified.\n"
                "• Refer to the manufacturer's documentation for the intended purpose."
            ),
            "usage_instructions": (
                "• Follow the verified product manual.\n"
                "• Confirm the correct operating procedure before use.\n"
                "• Maintain the equipment according to manufacturer guidance."
            ),
            "precautions": (
                "• Do not publish unverified medical or therapeutic claims.\n"
                "• Follow the manufacturer's safety instructions.\n"
                "• Confirm the device's intended use before operating it."
            ),
            "is_featured": True,
            "is_active": True,
            "display_order": 2,
            "customer_needs": [],
            "body_parts": [],
            "service_types": [],
            "intended_uses": [],
        },
    },
    {
        "category": {
            "name": "EMS & Muscle Stimulation Equipment",
            "slug": "ems-muscle-stimulation-equipment",
            "description": "",
            "display_order": 3,
            "is_active": True,
        },
        "service": {
            "name": "Electrical Muscle Stimulation (EMS)",
            "slug": "electrical-muscle-stimulation-ems",
            "short_description": "An electrical muscle stimulation device. Available programs, specifications and intended use depend on the actual model.",
            "description": (
                "Explore the Electrical Muscle Stimulation (EMS) equipment listed in the Rudra Massage & Wellness catalogue.\n\n"
                "EMS devices deliver electrical stimulation through electrodes according to the design of the specific product. "
                "The actual model's intended purpose, permitted settings, electrode placement instructions and safety requirements must be confirmed from its documentation.\n\n"
                "Contact our team for verified product specifications and availability."
            ),
            "benefits": (
                "• Intended function depends on the specific EMS device.\n"
                "• Use only for purposes specified by the manufacturer."
            ),
            "usage_instructions": (
                "• Read the complete user manual before operation.\n"
                "• Follow the manufacturer's instructions for electrode placement and settings.\n"
                "• Use only approved accessories."
            ),
            "precautions": (
                "• Read the complete user manual before operation.\n"
                "• Follow the manufacturer's instructions for electrode placement and settings.\n"
                "• Use only approved accessories."
            ),
            "is_featured": True,
            "is_active": True,
            "display_order": 2,
            "customer_needs": [],
            "body_parts": [],
            "service_types": ["Therapy Machines"],
            "intended_uses": ["Clinic/Centre", "Home Use"],
        },
    },
    {
        "category": {
            "name": "Electrical Massage Equipment",
            "slug": "electrical-massage-equipment",
            "description": "",
            "display_order": 4,
            "is_active": True,
        },
        "service": {
            "name": "Electro Pulse Massager Machine",
            "slug": "electro-pulse-massager",
            "short_description": "An electrical pulse massage device. Confirm its operating modes, supported applications and specifications from the actual product documentation.",
            "description": (
                "The Electro Pulse Massager Machine is listed in the Rudra Massage & Wellness catalogue.\n\n"
                "The precise technology, electrical output, available settings and intended use should be confirmed for the actual model. "
                "Provide customers with accurate operating instructions, included accessories, maintenance guidance and applicable safety information.\n\n"
                "Contact our team for product specifications and availability."
            ),
            "benefits": (
                "• Intended use depends on the device's design and manufacturer specifications.\n"
                "• Do not assume that the product treats a medical condition without verified supporting evidence."
            ),
            "usage_instructions": (
                "• Read the supplied manual before use.\n"
                "• Follow the manufacturer's instructions for settings and accessories.\n"
                "• Inspect the device and cables before operation."
            ),
            "precautions": (
                "• Follow all electrical safety instructions.\n"
                "• Do not use damaged cables or accessories.\n"
                "• Follow the manufacturer's contraindications for electrical stimulation.\n"
                "• Stop use if unexpected discomfort occurs."
            ),
            "is_featured": True,
            "is_active": True,
            "display_order": 2,
            "customer_needs": [],
            "body_parts": [],
            "service_types": ["Massagers", "Therapy Machines"],
            "intended_uses": [],
        },
    },
]


def seed_admin_user() -> bool:
    """
    Creates or updates the admin superuser with proper credentials.
    """
    User = get_user_model()
    username = ADMIN_CREDENTIALS["username"]
    email = ADMIN_CREDENTIALS["email"]
    password = ADMIN_CREDENTIALS["password"]

    try:
        with transaction.atomic():
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    "email": email,
                    "is_staff": True,
                    "is_superuser": True,
                },
            )

            # Ensure credentials and admin flags are synchronized
            user.email = email
            user.is_staff = True
            user.is_superuser = True
            user.set_password(password)
            user.save()

            action = "Created new" if created else "Updated existing"
            print(f"[OK] {action} superuser: '{username}' ({email})")
            return True

    except (DatabaseError, Exception) as exc:
        print(f"[ERROR] Failed to seed superuser '{username}': {exc}")
        return False


def seed_existing_services() -> bool:
    """
    Seeds the 5 existing services and categories without creating new/unverified data.
    """
    success = True

    for entry in EXISTING_SERVICES_DATA:
        cat_data = entry["category"]
        srv_data = entry["service"]

        try:
            with transaction.atomic():
                # 1. Category
                category, cat_created = Category.objects.update_or_create(
                    slug=cat_data["slug"],
                    defaults={
                        "name": cat_data["name"],
                        "description": cat_data.get("description", ""),
                        "display_order": cat_data.get("display_order", 0),
                        "is_active": cat_data.get("is_active", True),
                    },
                )

                # 2. Service
                service, srv_created = Service.objects.update_or_create(
                    slug=srv_data["slug"],
                    defaults={
                        "category": category,
                        "name": srv_data["name"],
                        "short_description": srv_data["short_description"],
                        "description": srv_data["description"],
                        "benefits": srv_data["benefits"],
                        "usage_instructions": srv_data["usage_instructions"],
                        "precautions": srv_data["precautions"],
                        "is_featured": srv_data["is_featured"],
                        "is_active": srv_data["is_active"],
                        "display_order": srv_data["display_order"],
                    },
                )

                # 3. Many-to-Many Taxonomies
                # Customer Needs
                needs_objs = [
                    CustomerNeed.objects.get_or_create(name=name)[0]
                    for name in srv_data.get("customer_needs", [])
                ]
                service.customer_needs.set(needs_objs)

                # Body Parts
                body_parts_objs = [
                    BodyPart.objects.get_or_create(name=name)[0]
                    for name in srv_data.get("body_parts", [])
                ]
                service.body_parts.set(body_parts_objs)

                # Service Types
                types_objs = [
                    ServiceType.objects.get_or_create(name=name)[0]
                    for name in srv_data.get("service_types", [])
                ]
                service.service_types.set(types_objs)

                # Intended Uses
                uses_objs = [
                    IntendedUse.objects.get_or_create(name=name)[0]
                    for name in srv_data.get("intended_uses", [])
                ]
                service.intended_uses.set(uses_objs)

                status = "Created" if srv_created else "Verified/Updated"
                print(f"[OK] {status} Service: '{service.name}' ({category.name})")

        except (DatabaseError, Exception) as exc:
            print(f"[ERROR] Failed to seed service '{srv_data.get('name', 'Unknown')}': {exc}")
            success = False

    return success


def seed_site_settings() -> bool:
    """
    Ensures the singleton SiteSettings record exists with valid default data.
    """
    try:
        with transaction.atomic():
            settings_obj = SiteSettings.load()
            print(f"[OK] Verified SiteSettings: '{settings_obj.business_name}'")
            return True
    except (DatabaseError, Exception) as exc:
        print(f"[ERROR] Failed to verify SiteSettings: {exc}")
        return False


def main():
    print("=" * 60)
    print("Rudra Massage & Wellness - Data Seeder")
    print("=" * 60)

    admin_ok = seed_admin_user()
    services_ok = seed_existing_services()
    settings_ok = seed_site_settings()

    print("-" * 60)
    if admin_ok and services_ok and settings_ok:
        print("Seeding completed successfully with 0 errors.")
        sys.exit(0)
    else:
        print("Seeding completed with one or more errors.")
        sys.exit(1)


if __name__ == "__main__":
    main()
