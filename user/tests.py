from datetime import timedelta
from django.contrib import admin
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import Client, TestCase
from django.utils import timezone
from django.urls import reverse

from .admin import (
    AnnouncementAdmin,
    AppointmentAdmin,
    CategoryAdmin,
    CustomerNeedAdmin,
    EnquiryAdmin,
    OfferAdmin,
    ServiceAdmin,
)
from .models import (
    Announcement,
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


class ServicesFilterAndSearchTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('user:services')

        # Categories
        self.cat_active = Category.objects.create(name='Therapy Machines', slug='therapy-machines', is_active=True)
        self.cat_inactive = Category.objects.create(name='Discontinued Category', slug='discontinued', is_active=False)

        # Filters
        self.need_back = CustomerNeed.objects.create(name='Back Pain', slug='back-pain', is_active=True)
        self.need_knee = CustomerNeed.objects.create(name='Knee Pain', slug='knee-pain', is_active=True)
        self.need_inactive = CustomerNeed.objects.create(name='Inactive Need', slug='inactive-need', is_active=False)

        self.body_back = BodyPart.objects.create(name='Back', slug='back', is_active=True)
        self.body_knee = BodyPart.objects.create(name='Knees', slug='knees', is_active=True)

        self.type_machine = ServiceType.objects.create(name='Therapy Machines', slug='therapy-machines', is_active=True)
        self.type_massager = ServiceType.objects.create(name='Massagers', slug='massagers', is_active=True)

        self.use_home = IntendedUse.objects.create(name='Home Use', slug='home-use', is_active=True)
        self.use_clinic = IntendedUse.objects.create(name='Clinic/Centre', slug='clinic-centre', is_active=True)

        # Service 1: Back relief unit
        self.s1 = Service.objects.create(
            category=self.cat_active,
            name='Spinal Traction Therapy Bed',
            slug='spinal-traction-therapy-bed',
            short_description='Dynamic lumbar decompression and thermal spinal relaxation.',
            description='Clinically engineered bed designed for soothing chronic back discomfort.',
            is_active=True,
            is_featured=True,
        )
        self.s1.customer_needs.add(self.need_back)
        self.s1.body_parts.add(self.body_back)
        self.s1.service_types.add(self.type_machine)
        self.s1.intended_uses.add(self.use_home, self.use_clinic)

        # Service 2: Knee massager
        self.s2 = Service.objects.create(
            category=self.cat_active,
            name='Knee Joint Infrared Warmth Massager',
            slug='knee-joint-infrared-warmth-massager',
            short_description='Pneumatic air pressure and heat wrap for stiff joints.',
            description='Targeted rehabilitation unit for patellar mobility and knee comfort.',
            is_active=True,
            is_featured=False,
        )
        self.s2.customer_needs.add(self.need_knee)
        self.s2.body_parts.add(self.body_knee)
        self.s2.service_types.add(self.type_massager)
        self.s2.intended_uses.add(self.use_home)

        # Service 3: Inactive Service
        self.s3_inactive = Service.objects.create(
            category=self.cat_active,
            name='Deactivated Therapy Unit',
            slug='deactivated-therapy-unit',
            short_description='Hidden unit.',
            description='Should never be visible.',
            is_active=False,
        )
        self.s3_inactive.customer_needs.add(self.need_back)

        # Service 4: Active service under inactive category
        self.s4_under_inactive_cat = Service.objects.create(
            category=self.cat_inactive,
            name='Orphaned Active Service',
            slug='orphaned-active-service',
            short_description='Belongs to inactive category.',
            description='Should not be visible.',
            is_active=True,
        )

    def test_services_page_loads_successfully(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Spinal Traction Therapy Bed')
        self.assertContains(response, 'Knee Joint Infrared Warmth Massager')
        self.assertNotContains(response, 'Deactivated Therapy Unit')
        self.assertNotContains(response, 'Orphaned Active Service')

    def test_search_by_name(self):
        response = self.client.get(self.url, {'q': 'Spinal'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Spinal Traction Therapy Bed')
        self.assertNotContains(response, 'Knee Joint Infrared Warmth Massager')

    def test_search_by_description(self):
        response = self.client.get(self.url, {'q': 'pneumatic'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Knee Joint Infrared Warmth Massager')
        self.assertNotContains(response, 'Spinal Traction Therapy Bed')

    def test_search_whitespace_handling(self):
        response = self.client.get(self.url, {'q': '   Spinal   '})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Spinal Traction Therapy Bed')

    def test_customer_need_filter_independent(self):
        response = self.client.get(self.url, {'need': ['back-pain']})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Spinal Traction Therapy Bed')
        self.assertNotContains(response, 'Knee Joint Infrared Warmth Massager')

    def test_body_part_filter_independent(self):
        response = self.client.get(self.url, {'body': ['knees']})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Knee Joint Infrared Warmth Massager')
        self.assertNotContains(response, 'Spinal Traction Therapy Bed')

    def test_service_type_filter_independent(self):
        response = self.client.get(self.url, {'type': ['therapy-machines']})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Spinal Traction Therapy Bed')
        self.assertNotContains(response, 'Knee Joint Infrared Warmth Massager')

    def test_intended_use_filter_independent(self):
        response = self.client.get(self.url, {'usage': ['clinic-centre']})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Spinal Traction Therapy Bed')
        self.assertNotContains(response, 'Knee Joint Infrared Warmth Massager')

    def test_combined_filters(self):
        # Match s1: need=back-pain AND body=back AND type=therapy-machines AND usage=home-use
        response = self.client.get(self.url, {
            'need': ['back-pain'],
            'body': ['back'],
            'type': ['therapy-machines'],
            'usage': ['home-use'],
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Spinal Traction Therapy Bed')
        self.assertNotContains(response, 'Knee Joint Infrared Warmth Massager')

    def test_combined_keyword_and_filters_no_match(self):
        # Searching 'Knee' but with 'back-pain' filter should return empty state
        response = self.client.get(self.url, {
            'q': 'Knee',
            'need': ['back-pain'],
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No matching solutions found')
        self.assertEqual(len(response.context['services']), 0)

    def test_no_duplicate_services(self):
        # When service matches multiple filters or joins, it must appear only once
        response = self.client.get(self.url, {'usage': ['home-use', 'clinic-centre']})
        self.assertEqual(response.status_code, 200)
        services_list = list(response.context['services'])
        s1_occurrences = [s for s in services_list if s.id == self.s1.id]
        self.assertEqual(len(s1_occurrences), 1)

    def test_inactive_filter_options_not_displayed(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Inactive Need')

    def test_invalid_filter_inputs_handled_safely(self):
        # Strange strings, SQL injection attempts, or non-existent slugs should not 500
        response = self.client.get(self.url, {
            'q': "'' OR '1'='1",
            'need': ['non-existent-slug-123', '$$$invalid'],
            'body': ['999999'],
            'type': ["' OR 1=1 --"],
            'usage': ['invalid-usage'],
            'sort': 'unknown-sort',
            'page': 'invalid-page',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No matching solutions found')


class ServiceDetailViewTests(TestCase):
    def setUp(self):
        self.client = Client()

        self.category_active = Category.objects.create(
            name='Ayurvedic Machines',
            slug='ayurvedic-machines',
            is_active=True,
            display_order=1,
        )
        self.category_inactive = Category.objects.create(
            name='Discontinued Line',
            slug='discontinued-line',
            is_active=False,
            display_order=2,
        )

        self.service_active = Service.objects.create(
            category=self.category_active,
            name='Shirodhara Machine Pro',
            slug='shirodhara-machine-pro',
            short_description='Continuous automated oil flow system.',
            description='Authentic therapy system engineered for soothing cranial treatments.',
            benefits='Relieves chronic stress, anxiety, and enhances sleep quality.',
            usage_instructions='Fill the oil basin, set the flow valve, and preheat gently.',
            precautions='Do not use during acute scalp infections or high fever.',
            is_active=True,
            is_featured=True,
        )

        self.service_related = Service.objects.create(
            category=self.category_active,
            name='Kansa Herbal Vatika Basin',
            slug='kansa-herbal-vatika-basin',
            short_description='Traditional bronze basin for oil collection.',
            description='Handcrafted pure bronze vatika bowl.',
            is_active=True,
            is_featured=False,
        )

        self.service_inactive = Service.objects.create(
            category=self.category_active,
            name='Retired Steam Box',
            slug='retired-steam-box',
            short_description='Old model.',
            description='Inactive model description.',
            is_active=False,
        )

        self.service_inactive_category = Service.objects.create(
            category=self.category_inactive,
            name='Orphaned Unit',
            slug='orphaned-unit',
            short_description='Belongs to inactive category.',
            description='Under inactive category description.',
            is_active=True,
        )

    def test_active_service_detail_success(self):
        url = reverse('user:service_detail', kwargs={'slug': self.service_active.slug})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'service-detail.html')
        self.assertEqual(response.context['service'], self.service_active)

        # Check core content rendering
        self.assertContains(response, 'Shirodhara Machine Pro')
        self.assertContains(response, 'Ayurvedic Machines')
        self.assertContains(response, 'Continuous automated oil flow system.')
        self.assertContains(response, 'Authentic therapy system engineered for soothing cranial treatments.')
        self.assertContains(response, 'Relieves chronic stress, anxiety, and enhances sleep quality.')
        self.assertContains(response, 'Fill the oil basin, set the flow valve, and preheat gently.')
        self.assertContains(response, 'Do not use during acute scalp infections or high fever.')

        # Check call-to-actions
        self.assertContains(response, f"/appointment/?service={self.service_active.id}")
        self.assertContains(response, f"/enquiry/?service={self.service_active.id}")

    def test_unknown_slug_returns_404(self):
        url = reverse('user:service_detail', kwargs={'slug': 'non-existent-therapy-slug'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_inactive_service_returns_404(self):
        url = reverse('user:service_detail', kwargs={'slug': self.service_inactive.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_service_with_inactive_category_returns_404(self):
        url = reverse('user:service_detail', kwargs={'slug': self.service_inactive_category.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_related_services_rendered(self):
        url = reverse('user:service_detail', kwargs={'slug': self.service_active.slug})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        related = list(response.context['related_services'])
        self.assertIn(self.service_related, related)
        self.assertNotIn(self.service_active, related)
        self.assertNotIn(self.service_inactive, related)
        self.assertNotIn(self.service_inactive_category, related)
        self.assertContains(response, 'Kansa Herbal Vatika Basin')

    def test_services_list_links_to_slug_detail_page(self):
        services_url = reverse('user:services')
        response = self.client.get(services_url)

        self.assertEqual(response.status_code, 200)
        detail_url = reverse('user:service_detail', kwargs={'slug': self.service_active.slug})
        self.assertContains(response, detail_url)


class AdminConfigurationTests(TestCase):
    def setUp(self):
        self.site = admin.site

    def test_all_models_registered_in_admin(self):
        for model in [Category, Service, CustomerNeed, BodyPart, ServiceType, IntendedUse, Offer, Announcement, Enquiry]:
            self.assertIn(model, self.site._registry)

    def test_enquiry_admin_options(self):
        ma = self.site._registry[Enquiry]
        self.assertIsInstance(ma, EnquiryAdmin)
        self.assertIn("name", ma.list_display)
        self.assertIn("phone", ma.list_display)
        self.assertIn("status", ma.list_display)
        self.assertIn("status", ma.list_editable)
        self.assertIn("status", ma.list_filter)
        self.assertIn("created_at", ma.list_filter)
        self.assertIn("created_at", ma.readonly_fields)
        self.assertIn("updated_at", ma.readonly_fields)
        self.assertIn("name", ma.search_fields)
        self.assertIn("phone", ma.search_fields)
        self.assertIn("email", ma.search_fields)

    def test_category_admin_options(self):
        ma = self.site._registry[Category]
        self.assertIsInstance(ma, CategoryAdmin)
        self.assertIn("image_preview", ma.list_display)
        self.assertIn("service_count", ma.list_display)
        self.assertIn("is_active", ma.list_editable)
        self.assertIn("display_order", ma.list_editable)
        self.assertIn("slug", ma.prepopulated_fields)

    def test_service_admin_options(self):
        ma = self.site._registry[Service]
        self.assertIsInstance(ma, ServiceAdmin)
        self.assertIn("image_preview", ma.list_display)
        self.assertIn("category__name", ma.search_fields)
        self.assertIn("customer_needs", ma.filter_horizontal)
        self.assertIn("body_parts", ma.filter_horizontal)
        self.assertIn("service_types", ma.filter_horizontal)
        self.assertIn("intended_uses", ma.filter_horizontal)
        self.assertIn("created_at", ma.readonly_fields)
        self.assertIn("updated_at", ma.readonly_fields)
        self.assertIn("image_preview_detail", ma.readonly_fields)
        # Ensure fieldsets are defined
        self.assertTrue(len(ma.fieldsets) >= 4)

    def test_filter_admins_service_count(self):
        ma = self.site._registry[CustomerNeed]
        self.assertIsInstance(ma, CustomerNeedAdmin)
        self.assertIn("service_count", ma.list_display)

    def test_offer_admin_status_badge(self):
        ma = self.site._registry[Offer]
        self.assertIsInstance(ma, OfferAdmin)
        now = timezone.now()

        active_offer = Offer.objects.create(
            title="Active Offer",
            discount_title="10% OFF",
            description="Active test",
            is_active=True,
        )
        scheduled_offer = Offer.objects.create(
            title="Scheduled Offer",
            discount_title="15% OFF",
            description="Scheduled test",
            is_active=True,
            valid_from=now + timedelta(days=2),
        )
        expired_offer = Offer.objects.create(
            title="Expired Offer",
            discount_title="20% OFF",
            description="Expired test",
            is_active=True,
            valid_until=now - timedelta(days=1),
        )
        inactive_offer = Offer.objects.create(
            title="Inactive Offer",
            discount_title="25% OFF",
            description="Inactive test",
            is_active=False,
        )

        self.assertIn("Active", ma.status_badge(active_offer))
        self.assertIn("Scheduled", ma.status_badge(scheduled_offer))
        self.assertIn("Expired", ma.status_badge(expired_offer))
        self.assertIn("Inactive", ma.status_badge(inactive_offer))

    def test_announcement_admin_status_badge(self):
        ma = self.site._registry[Announcement]
        self.assertIsInstance(ma, AnnouncementAdmin)
        now = timezone.now()

        active_announcement = Announcement.objects.create(
            message="Active Announcement",
            is_active=True,
        )
        inactive_announcement = Announcement.objects.create(
            message="Inactive Announcement",
            is_active=False,
        )

        self.assertIn("Active", ma.status_badge(active_announcement))
        self.assertIn("Inactive", ma.status_badge(inactive_announcement))


class SlugPreservationAndValidationTests(TestCase):
    def test_category_slug_auto_generated_when_empty(self):
        cat = Category.objects.create(name="Ayurvedic Accessories")
        self.assertEqual(cat.slug, "ayurvedic-accessories")

    def test_category_custom_slug_not_overwritten(self):
        cat = Category.objects.create(name="Herbal Powders", slug="custom-herbal-slug")
        cat.name = "Herbal Powders Premium"
        cat.save()
        self.assertEqual(cat.slug, "custom-herbal-slug")

    def test_service_slug_auto_generated_when_empty(self):
        cat = Category.objects.create(name="Bedding")
        service = Service.objects.create(
            category=cat,
            name="Ortho Comfort Mattress",
            short_description="Short desc",
            description="Long desc",
        )
        self.assertEqual(service.slug, "ortho-comfort-mattress")

    def test_service_custom_slug_not_overwritten(self):
        cat = Category.objects.create(name="Bedding 2")
        service = Service.objects.create(
            category=cat,
            name="Cervical Pillow",
            slug="special-cervical-pillow",
            short_description="Short desc",
            description="Long desc",
        )
        service.name = "Cervical Pillow Deluxe"
        service.save()
        self.assertEqual(service.slug, "special-cervical-pillow")

    def test_category_whitespace_validation(self):
        cat = Category(name="   ", slug="test-cat")
        with self.assertRaises(ValidationError):
            cat.clean()

    def test_service_whitespace_validation(self):
        cat = Category.objects.create(name="Valid Cat", slug="valid-cat")
        s = Service(
            category=cat,
            name="  ",
            slug="test-service",
            short_description="Short desc",
            description="Long desc",
        )
        with self.assertRaises(ValidationError):
            s.clean()

    def test_offer_invalid_date_range_validation(self):
        now = timezone.now()
        offer = Offer(
            title="Invalid Date Offer",
            discount_title="50% OFF",
            description="Test description",
            valid_from=now + timedelta(days=5),
            valid_until=now + timedelta(days=1),
        )
        with self.assertRaises(ValidationError):
            offer.clean()

    def test_announcement_invalid_date_range_validation(self):
        now = timezone.now()
        announcement = Announcement(
            message="Invalid date announcement",
            valid_from=now + timedelta(days=5),
            valid_until=now + timedelta(days=1),
        )
        with self.assertRaises(ValidationError):
            announcement.clean()


class OfferManagementAndPublicViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('user:offers')
        now = timezone.now()

        # Active current offer
        self.active_offer = Offer.objects.create(
            title="Spring Detox Sale",
            badge_tag="Spring Special",
            discount_title="Flat 30% OFF",
            description="Great savings on herbal steamers.",
            promo_code="SPRING30",
            validity_text="Valid this month",
            is_active=True,
            display_order=1,
        )

        # Inactive offer (should not be shown)
        self.inactive_offer = Offer.objects.create(
            title="Old Deactivated Promo",
            discount_title="50% OFF",
            description="Should never appear.",
            promo_code="INACTIVE50",
            is_active=False,
            display_order=2,
        )

        # Expired offer (should not be shown)
        self.expired_offer = Offer.objects.create(
            title="Past Diwali Special",
            discount_title="40% OFF",
            description="Expired past campaign.",
            promo_code="PAST40",
            valid_from=now - timedelta(days=30),
            valid_until=now - timedelta(days=5),
            is_active=True,
            display_order=3,
        )

        # Scheduled future offer (should not be shown)
        self.future_offer = Offer.objects.create(
            title="Upcoming New Year Bonanza",
            discount_title="35% OFF",
            description="Coming soon.",
            promo_code="FUTURE35",
            valid_from=now + timedelta(days=10),
            valid_until=now + timedelta(days=20),
            is_active=True,
            display_order=4,
        )

    def test_offers_page_renders_only_active_valid_offers(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        # Active offer must be present
        self.assertContains(response, "Spring Detox Sale")
        self.assertContains(response, "Flat 30% OFF")
        self.assertContains(response, "SPRING30")
        self.assertContains(response, "Spring Special")

        # Inactive, expired, and future offers must NOT be present
        self.assertNotContains(response, "Old Deactivated Promo")
        self.assertNotContains(response, "Past Diwali Special")
        self.assertNotContains(response, "Upcoming New Year Bonanza")

    def test_offers_page_empty_state_when_no_active_offers(self):
        Offer.objects.all().delete()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No Active Offers Right Now")


class AnnouncementContextAndDisplayTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.home_url = reverse('user:home')
        now = timezone.now()

        self.announcement = Announcement.objects.create(
            message="Winter Wellness: Flat 20% OFF on all massagers.",
            badge_text="Winter Sale",
            link_text="View Deals →",
            link_url="/offers/",
            is_active=True,
            display_order=1,
        )

    def test_active_announcement_renders_in_header(self):
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Winter Wellness: Flat 20% OFF on all massagers.")
        self.assertContains(response, "Winter Sale:")
        self.assertContains(response, "View Deals →")

    def test_inactive_announcement_is_hidden(self):
        self.announcement.is_active = False
        self.announcement.save()

        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Winter Wellness: Flat 20% OFF on all massagers.")
        self.assertNotContains(response, "announcement-bar")

    def test_expired_announcement_is_hidden(self):
        now = timezone.now()
        self.announcement.valid_until = now - timedelta(hours=1)
        self.announcement.save()

        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Winter Wellness: Flat 20% OFF on all massagers.")
        self.assertNotContains(response, "announcement-bar")

    def test_scheduled_future_announcement_is_hidden(self):
        now = timezone.now()
        self.announcement.valid_from = now + timedelta(days=2)
        self.announcement.save()

        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Winter Wellness: Flat 20% OFF on all massagers.")
        self.assertNotContains(response, "announcement-bar")


class EnquiryWorkflowAndValidationTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.enquiry_url = reverse('user:enquiry')

        self.category = Category.objects.create(
            name="Therapy Devices",
            slug="therapy-devices",
            is_active=True,
        )
        self.inactive_category = Category.objects.create(
            name="Legacy Devices",
            slug="legacy-devices",
            is_active=False,
        )

        self.active_service = Service.objects.create(
            category=self.category,
            name="Decompression Spinal Belt",
            slug="decompression-spinal-belt",
            short_description="Lumbar support",
            description="Detailed lumbar support machine",
            is_active=True,
        )
        self.inactive_service = Service.objects.create(
            category=self.category,
            name="Retired Traction Bed",
            slug="retired-traction-bed",
            short_description="Inactive machine",
            description="Detailed inactive machine",
            is_active=False,
        )
        self.service_under_inactive_category = Service.objects.create(
            category=self.inactive_category,
            name="Orphaned Steamer",
            slug="orphaned-steamer",
            short_description="Under inactive category",
            description="Detailed description",
            is_active=True,
        )

    def test_enquiry_page_loads_with_active_services(self):
        response = self.client.get(self.enquiry_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Decompression Spinal Belt")
        self.assertNotContains(response, "Retired Traction Bed")
        self.assertNotContains(response, "Orphaned Steamer")

    def test_valid_enquiry_submission_success(self):
        post_data = {
            "name": "Ramesh Patel",
            "phone": "98250 12345",
            "email": "ramesh@example.com",
            "city": "Ahmedabad",
            "service": str(self.active_service.id),
            "usage_intention": "clinic",
            "callback_time": "afternoon",
            "message": "Interested in bulk demo.",
        }
        response = self.client.post(self.enquiry_url, post_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Your enquiry has been received")

        # Database verification
        self.assertEqual(Enquiry.objects.count(), 1)
        enq = Enquiry.objects.first()
        self.assertEqual(enq.name, "Ramesh Patel")
        self.assertEqual(enq.phone, "9825012345")
        self.assertEqual(enq.email, "ramesh@example.com")
        self.assertEqual(enq.city, "Ahmedabad")
        self.assertEqual(enq.service, self.active_service)
        self.assertEqual(enq.service_name_snapshot, "Decompression Spinal Belt")
        self.assertEqual(enq.usage_intention, "clinic")
        self.assertEqual(enq.callback_time, "afternoon")
        self.assertEqual(enq.status, Enquiry.Status.NEW)

    def test_optional_email_submission(self):
        post_data = {
            "name": "Bhavik Shah",
            "phone": "+91 97240 54321",
            "email": "",
            "city": "Surat",
            "service": "",
            "usage_intention": "personal",
            "callback_time": "morning",
            "message": "",
        }
        response = self.client.post(self.enquiry_url, post_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Your enquiry has been received")

        self.assertEqual(Enquiry.objects.count(), 1)
        enq = Enquiry.objects.first()
        self.assertEqual(enq.name, "Bhavik Shah")
        self.assertEqual(enq.phone, "9724054321")
        self.assertEqual(enq.email, "")
        self.assertIsNone(enq.service)

    def test_invalid_phone_number_rejected(self):
        post_data = {
            "name": "Ramesh Patel",
            "phone": "123456",
            "email": "ramesh@example.com",
            "city": "Ahmedabad",
        }
        response = self.client.post(self.enquiry_url, post_data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Please enter a valid 10-digit Indian mobile number")
        self.assertEqual(Enquiry.objects.count(), 0)

    def test_missing_required_fields_rejected(self):
        post_data = {
            "name": "",
            "phone": "",
            "city": "",
        }
        response = self.client.post(self.enquiry_url, post_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Enquiry.objects.count(), 0)

    def test_service_preselection_via_query_param(self):
        url = f"{self.enquiry_url}?service={self.active_service.id}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["selected_service"], self.active_service)
        self.assertContains(response, f'value="{self.active_service.id}" selected')

    def test_invalid_service_id_in_get_param_handled_safely(self):
        url_non_existent = f"{self.enquiry_url}?service=999999"
        response = self.client.get(url_non_existent)
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(response.context["selected_service"])

        url_alphabetic = f"{self.enquiry_url}?service=invalid-slug-here"
        response2 = self.client.get(url_alphabetic)
        self.assertEqual(response2.status_code, 200)
        self.assertIsNone(response2.context["selected_service"])

    def test_invalid_service_id_in_post_rejected(self):
        post_data = {
            "name": "Kavita Joshi",
            "phone": "98980 12345",
            "city": "Vadodara",
            "service": "999999",
        }
        response = self.client.post(self.enquiry_url, post_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Enquiry.objects.count(), 0)

    def test_inactive_service_in_post_rejected(self):
        post_data = {
            "name": "Kavita Joshi",
            "phone": "98980 12345",
            "city": "Vadodara",
            "service": str(self.inactive_service.id),
        }
        response = self.client.post(self.enquiry_url, post_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Enquiry.objects.count(), 0)

    def test_duplicate_submission_prevention(self):
        post_data = {
            "name": "Hiren Dave",
            "phone": "99240 11223",
            "city": "Rajkot",
            "service": str(self.active_service.id),
            "message": "Testing duplicate prevention.",
        }
        # First submission
        res1 = self.client.post(self.enquiry_url, post_data, follow=True)
        self.assertEqual(res1.status_code, 200)
        self.assertEqual(Enquiry.objects.count(), 1)

        # Immediate second submission (same phone & service within 2 minutes)
        res2 = self.client.post(self.enquiry_url, post_data, follow=True)
        self.assertEqual(res2.status_code, 200)
        self.assertContains(res2, "We have already received your enquiry recently")
        self.assertEqual(Enquiry.objects.count(), 1)

    def test_enquiry_status_update_via_admin(self):
        admin_user = User.objects.create_superuser(
            username="adminuser",
            email="admin@rudra.com",
            password="adminpassword123",
        )
        self.client.login(username="adminuser", password="adminpassword123")

        enq = Enquiry.objects.create(
            name="Direct Enquiry",
            phone="9876543210",
            city="Gandhinagar",
            service=self.active_service,
            status=Enquiry.Status.NEW,
        )

        admin_change_url = reverse("admin:user_enquiry_change", args=[enq.id])
        post_data = {
            "name": enq.name,
            "phone": enq.phone,
            "email": enq.email,
            "city": enq.city,
            "service": str(self.active_service.id),
            "service_name_snapshot": enq.service_name_snapshot,
            "usage_intention": enq.usage_intention,
            "callback_time": enq.callback_time,
            "message": enq.message,
            "status": Enquiry.Status.CONTACTED,
            "admin_notes": "Called client, shared catalogue via WhatsApp.",
        }
        response = self.client.post(admin_change_url, post_data)
        self.assertEqual(response.status_code, 302)

        enq.refresh_from_db()
        self.assertEqual(enq.status, Enquiry.Status.CONTACTED)
        self.assertEqual(enq.admin_notes, "Called client, shared catalogue via WhatsApp.")

    def test_unauthorized_access_restrictions(self):
        # Anonymous access to Django admin enquiry list must redirect to admin login
        admin_list_url = reverse("admin:user_enquiry_changelist")
        response = self.client.get(admin_list_url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("login", response.url)

        # Anonymous access to custom-admin enquiries must redirect to admin login
        custom_admin_url = reverse("custom_admin:enquiries")
        response_ca = self.client.get(custom_admin_url)
        self.assertEqual(response_ca.status_code, 302)
        self.assertIn("login", response_ca.url)

        # Authenticated staff user has access
        staff_user = User.objects.create_superuser(
            username="stafflead",
            email="staff@rudra.com",
            password="staffpassword123",
        )
        self.client.login(username="stafflead", password="staffpassword123")
        response_staff = self.client.get(custom_admin_url)
        self.assertEqual(response_staff.status_code, 200)

    def test_enquiry_with_enquiry_type_and_contact_method(self):
        post_data = {
            "name": "Pooja Trivedi",
            "phone": "98241 23456",
            "email": "pooja@example.com",
            "city": "Ahmedabad",
            "enquiry_type": "home_setup",
            "service": str(self.active_service.id),
            "usage_intention": "personal",
            "callback_time": "morning",
            "preferred_contact_method": "whatsapp",
            "message": "Looking for home setup advice.",
        }
        response = self.client.post(self.enquiry_url, post_data, follow=True)
        self.assertEqual(response.status_code, 200)
        enq = Enquiry.objects.filter(phone="9824123456").first()
        self.assertIsNotNone(enq)
        self.assertEqual(enq.enquiry_type, "home_setup")
        self.assertEqual(enq.preferred_contact_method, "whatsapp")


class AppointmentWorkflowAndValidationTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.appointment_url = reverse('user:appointment')
        self.admin_appointment_url = reverse('custom_admin:appointments')

        self.category = Category.objects.create(
            name="Therapy Machines",
            slug="therapy-machines",
            is_active=True,
        )
        self.inactive_category = Category.objects.create(
            name="Discontinued Machines",
            slug="discontinued-machines",
            is_active=False,
        )

        self.active_service = Service.objects.create(
            category=self.category,
            name="AyurSpine Decompression Belt",
            slug="ayurspine-decompression-belt",
            short_description="Lumbar traction",
            description="Clinical spine relaxation machine",
            is_active=True,
        )
        self.inactive_service = Service.objects.create(
            category=self.category,
            name="Retired Roller Bed",
            slug="retired-roller-bed",
            short_description="Retired roller",
            description="Inactive roller bed",
            is_active=False,
        )

        self.staff_user = User.objects.create_superuser(
            username="appointment_staff",
            email="apt_staff@rudra.com",
            password="staffpassword123",
        )
        self.initial_count = Appointment.objects.count()

    def test_appointment_page_loads_with_active_services(self):
        response = self.client.get(self.appointment_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Book Your Appointment")
        self.assertContains(response, "AyurSpine Decompression Belt")
        self.assertNotContains(response, "Retired Roller Bed")

    def test_service_preselection_via_query_param(self):
        url = f"{self.appointment_url}?service={self.active_service.id}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["selected_service"], self.active_service)
        self.assertContains(response, f'value="{self.active_service.id}" selected')

    def test_valid_appointment_booking_request_success(self):
        tomorrow = (timezone.localdate() + timedelta(days=1)).strftime("%Y-%m-%d")
        post_data = {
            "name": "Dr. Ankit Shah",
            "phone": "98251 98765",
            "email": "ankit@example.com",
            "city": "Surat",
            "service": str(self.active_service.id),
            "appointment_date": tomorrow,
            "time_slot": "morning",
            "demo_format": "home",
            "notes": "Doorstep demo at clinic premises.",
        }
        response = self.client.post(self.appointment_url, post_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Your appointment request")

        self.assertEqual(Appointment.objects.count(), self.initial_count + 1)
        apt = Appointment.objects.get(name="Dr. Ankit Shah")
        self.assertEqual(apt.name, "Dr. Ankit Shah")
        self.assertEqual(apt.phone, "9825198765")
        self.assertEqual(apt.email, "ankit@example.com")
        self.assertEqual(apt.city, "Surat")
        self.assertEqual(apt.service, self.active_service)
        self.assertEqual(apt.service_name_snapshot, "AyurSpine Decompression Belt")
        self.assertEqual(apt.status, Appointment.Status.PENDING)
        self.assertTrue(apt.booking_reference.startswith("APT-"))

    def test_past_date_rejected(self):
        yesterday = (timezone.localdate() - timedelta(days=1)).strftime("%Y-%m-%d")
        post_data = {
            "name": "Late Visitor",
            "phone": "98251 98765",
            "city": "Surat",
            "service": str(self.active_service.id),
            "appointment_date": yesterday,
            "time_slot": "morning",
        }
        response = self.client.post(self.appointment_url, post_data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "cannot be in the past")
        self.assertEqual(Appointment.objects.count(), self.initial_count)

    def test_missing_required_fields_rejected(self):
        post_data = {
            "name": "",
            "phone": "",
            "city": "",
            "service": "",
            "appointment_date": "",
            "time_slot": "",
        }
        response = self.client.post(self.appointment_url, post_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Appointment.objects.count(), self.initial_count)

    def test_invalid_phone_rejected(self):
        tomorrow = (timezone.localdate() + timedelta(days=1)).strftime("%Y-%m-%d")
        post_data = {
            "name": "Invalid Phone User",
            "phone": "12345",
            "city": "Ahmedabad",
            "service": str(self.active_service.id),
            "appointment_date": tomorrow,
            "time_slot": "morning",
        }
        response = self.client.post(self.appointment_url, post_data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Please enter a valid 10-digit Indian mobile number")
        self.assertEqual(Appointment.objects.count(), self.initial_count)

    def test_duplicate_appointment_prevention(self):
        tomorrow = (timezone.localdate() + timedelta(days=1)).strftime("%Y-%m-%d")
        post_data = {
            "name": "Repeat Customer",
            "phone": "98980 88776",
            "city": "Rajkot",
            "service": str(self.active_service.id),
            "appointment_date": tomorrow,
            "time_slot": "morning",
        }
        # First submission succeeds
        res1 = self.client.post(self.appointment_url, post_data, follow=True)
        self.assertEqual(res1.status_code, 200)
        self.assertEqual(Appointment.objects.count(), self.initial_count + 1)

        # Immediate repeat within 2 minutes is flagged
        res2 = self.client.post(self.appointment_url, post_data, follow=True)
        self.assertEqual(res2.status_code, 200)
        self.assertContains(res2, "already received an appointment request")
        self.assertEqual(Appointment.objects.count(), self.initial_count + 1)
    def test_inactive_service_in_post_rejected(self):
        tomorrow = (timezone.localdate() + timedelta(days=1)).strftime("%Y-%m-%d")
        post_data = {
            "name": "Inactive Service Tester",
            "phone": "98980 12345",
            "city": "Ahmedabad",
            "service": str(self.inactive_service.id),
            "appointment_date": tomorrow,
            "time_slot": "morning",
        }
        response = self.client.post(self.appointment_url, post_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Appointment.objects.count(), self.initial_count)

    def test_status_and_admin_notes_protected_from_public_post(self):
        tomorrow = (timezone.localdate() + timedelta(days=1)).strftime("%Y-%m-%d")
        post_data = {
            "name": "Security Tester",
            "phone": "98251 11223",
            "email": "sec@example.com",
            "city": "Vadodara",
            "service": str(self.active_service.id),
            "appointment_date": tomorrow,
            "time_slot": "morning",
            "status": "confirmed",
            "admin_notes": "Attempted injection of internal staff notes",
        }
        response = self.client.post(self.appointment_url, post_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Appointment.objects.count(), self.initial_count + 1)
        apt = Appointment.objects.get(name="Security Tester")
        self.assertEqual(apt.status, Appointment.Status.PENDING)
        self.assertEqual(apt.admin_notes, "")

    def test_custom_admin_appointments_access_and_filter(self):
        # Anonymous redirect
        res_anon = self.client.get(self.admin_appointment_url)
        self.assertEqual(res_anon.status_code, 302)

        # Staff access
        self.client.login(username="appointment_staff", password="staffpassword123")
        apt = Appointment.objects.create(
            name="VIP Client",
            phone="9876543210",
            city="Ahmedabad",
            service=self.active_service,
            appointment_date=timezone.localdate() + timedelta(days=2),
            time_slot="midday",
            status=Appointment.Status.PENDING,
        )
        res_staff = self.client.get(self.admin_appointment_url)
        self.assertEqual(res_staff.status_code, 200)
        self.assertContains(res_staff, apt.booking_reference)
        self.assertContains(res_staff, "VIP Client")

        # Search filter
        res_search = self.client.get(f"{self.admin_appointment_url}?q=VIP")
        self.assertEqual(res_search.status_code, 200)
        self.assertContains(res_search, "VIP Client")

    def test_custom_admin_appointment_status_update(self):
        self.client.login(username="appointment_staff", password="staffpassword123")
        apt = Appointment.objects.create(
            name="Status Test Client",
            phone="9876543210",
            city="Ahmedabad",
            service=self.active_service,
            appointment_date=timezone.localdate() + timedelta(days=3),
            time_slot="afternoon",
            status=Appointment.Status.PENDING,
        )
        post_data = {
            "appointment_id": apt.id,
            "status": Appointment.Status.CONFIRMED,
            "admin_notes": "Confirmed over phone call.",
        }
        res = self.client.post(self.admin_appointment_url, post_data, follow=True)
        self.assertEqual(res.status_code, 200)

        apt.refresh_from_db()
        self.assertEqual(apt.status, Appointment.Status.CONFIRMED)
        self.assertEqual(apt.admin_notes, "Confirmed over phone call.")


class DatabaseDrivenAndNoDemoDataRegressionTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.staff_user = User.objects.create_superuser(
            username="regression_staff",
            email="staff@rudra.com",
            password="StaffPassword123!",
        )
        self.category = Category.objects.create(
            name="Vedic Steamers",
            slug="vedic-steamers",
            is_active=True,
        )
        self.service = Service.objects.create(
            category=self.category,
            name="Authentic Vedic Steam Chamber",
            slug="authentic-vedic-steam-chamber",
            short_description="Ayurvedic herb-infused steam box.",
            description="Deep cellular detox with classical steam therapy.",
            is_active=True,
            is_featured=True,
        )

    def test_fresh_database_has_no_demo_appointments(self):
        # Fresh test DB must not contain legacy migrated mock bookings
        demo_count = Appointment.objects.filter(
            booking_reference__in=["APT-401", "APT-402", "APT-403"]
        ).count()
        self.assertEqual(demo_count, 0)
        self.assertEqual(Appointment.objects.count(), 0)

    def test_cleanup_idempotency_preserves_real_appointments(self):
        # Create a real booking
        real_apt = Appointment.objects.create(
            booking_reference="APT-REAL-12345",
            name="Kuldipsinh Rathod",
            phone="9635986535",
            city="Ahmedabad",
            service=self.service,
            appointment_date=timezone.localdate() + timedelta(days=2),
            time_slot="morning",
            status=Appointment.Status.CONFIRMED,
        )

        # Run demo cleanup query again
        Appointment.objects.filter(
            booking_reference__in=["APT-401", "APT-402", "APT-403"]
        ).delete()

        # Confirm real booking is 100% preserved
        self.assertEqual(Appointment.objects.count(), 1)
        preserved = Appointment.objects.get(id=real_apt.id)
        self.assertEqual(preserved.booking_reference, "APT-REAL-12345")
        self.assertEqual(preserved.name, "Kuldipsinh Rathod")

    def test_custom_admin_appointment_empty_state_contains_no_demo_records(self):
        self.client.login(username="regression_staff", password="StaffPassword123!")
        url = reverse("custom_admin:appointments")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # Must display clear empty state
        self.assertContains(response, "No appointment bookings found")

        # Must never contain mock names or demo IDs
        self.assertNotContains(response, "APT-401")
        self.assertNotContains(response, "APT-402")
        self.assertNotContains(response, "APT-403")
        self.assertNotContains(response, "Sanjay Solanki")
        self.assertNotContains(response, "Dr. Hemal Bhatt")
        self.assertNotContains(response, "Geeta Desai")

    def test_custom_admin_enquiries_empty_state_contains_no_demo_records(self):
        self.client.login(username="regression_staff", password="StaffPassword123!")
        url = reverse("custom_admin:enquiries")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, "No customer enquiries found")
        self.assertNotContains(response, "ENQ-901")
        self.assertNotContains(response, "Kavita Shah")
        self.assertNotContains(response, "Bhavesh Mehtalia")

    def test_home_featured_services_are_database_driven(self):
        url = reverse("user:home")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # Real DB service rendered
        self.assertContains(response, "Authentic Vedic Steam Chamber")

        # No hardcoded mock product IDs
        self.assertNotContains(response, "wt-101")
        self.assertNotContains(response, "wt-102")
        self.assertNotContains(response, "wt-103")
        self.assertNotContains(response, "wt-104")

    def test_custom_admin_offers_and_announcements_database_driven(self):
        self.client.login(username="regression_staff", password="StaffPassword123!")
        url = reverse("custom_admin:offers")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # Empty state initially
        self.assertContains(response, "No promotional offers found in database.")
        self.assertContains(response, "No announcements found in database.")
        self.assertNotContains(response, "FESTIVE25")
        self.assertNotContains(response, "SENIORCARE")

        # Create real offer and announcement
        Offer.objects.create(
            promo_code="REALWELL20",
            title="Real Database Wellness Discount",
            discount_title="20% OFF",
            is_active=True,
        )
        Announcement.objects.create(
            badge_text="Live Update",
            message="Authentic Clinic Grand Reopening",
            is_active=True,
        )

        res2 = self.client.get(url)
        self.assertEqual(res2.status_code, 200)
        self.assertContains(res2, "REALWELL20")
        self.assertContains(res2, "Real Database Wellness Discount")
        self.assertContains(res2, "Authentic Clinic Grand Reopening")


class SiteSettingsModelAndSingletonTests(TestCase):
    def setUp(self):
        SiteSettings.objects.all().delete()

    def test_singleton_creation_and_enforcement(self):
        # Initial load creates the singleton record
        settings1 = SiteSettings.load()
        self.assertEqual(settings1.pk, 1)
        self.assertEqual(SiteSettings.objects.count(), 1)

        # Attempting to create another record still updates pk=1
        settings2 = SiteSettings(
            business_name="Secondary Entity",
            primary_phone="+91 91111 22222",
            contact_email="secondary@example.com",
            business_address="Secondary Address",
        )
        settings2.save()

        # Database still has only 1 record
        self.assertEqual(SiteSettings.objects.count(), 1)
        reloaded = SiteSettings.objects.first()
        self.assertEqual(reloaded.pk, 1)
        self.assertEqual(reloaded.business_name, "Secondary Entity")

    def test_whitespace_validation(self):
        settings = SiteSettings(
            business_name="   ",
            primary_phone="   ",
            contact_email="   ",
            business_address="   ",
        )
        with self.assertRaises(ValidationError):
            settings.full_clean()

    def test_delete_is_prevented(self):
        settings = SiteSettings.load()
        self.assertEqual(SiteSettings.objects.count(), 1)
        settings.delete()
        # Singleton record remains
        self.assertEqual(SiteSettings.objects.count(), 1)

    def test_helper_properties(self):
        settings = SiteSettings.load()
        settings.primary_phone = "+91 98250 12345"
        settings.whatsapp_number = "+91 (98250) 12345"
        self.assertEqual(settings.phone_digits, "+919825012345")
        self.assertEqual(settings.whatsapp_digits, "919825012345")


class SiteSettingsContextProcessorAndTemplateRenderingTests(TestCase):
    def setUp(self):
        self.client = Client()
        SiteSettings.objects.all().delete()
        self.settings = SiteSettings.objects.create(
            pk=1,
            business_name="Rudra Testing Sanctuary",
            primary_phone="+91 98765 00112",
            contact_email="support@rudratest.com",
            whatsapp_number="+91 98765 00112",
            business_address="Test Wing 4, SG Highway, Ahmedabad 380054",
            google_maps_url="https://maps.google.com/?q=TestAhmedabad",
            business_hours="Mon - Fri: 8:00 AM - 8:00 PM",
            enable_announcement_banner=True,
            enable_whatsapp_floating=True,
        )

    def test_header_footer_rendering_from_database_settings(self):
        response = self.client.get(reverse("user:home"))
        self.assertEqual(response.status_code, 200)
        # Context variable is present
        self.assertIn("site_settings", response.context)
        # Phone and email rendered in footer
        self.assertContains(response, "+91 98765 00112")
        self.assertContains(response, "support@rudratest.com")
        self.assertContains(response, "Test Wing 4, SG Highway, Ahmedabad 380054")
        self.assertContains(response, "Mon - Fri: 8:00 AM - 8:00 PM")
        self.assertContains(response, "Rudra Testing Sanctuary")

    def test_contact_page_renders_database_settings(self):
        response = self.client.get(reverse("user:contact"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "+91 98765 00112")
        self.assertContains(response, "support@rudratest.com")
        self.assertContains(response, "Test Wing 4, SG Highway, Ahmedabad 380054")
        self.assertContains(response, "https://maps.google.com/?q=TestAhmedabad")

    def test_floating_whatsapp_toggle_off_hides_button(self):
        self.settings.enable_whatsapp_floating = False
        self.settings.save()

        response = self.client.get(reverse("user:home"))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "whatsapp-floating")

    def test_announcement_banner_toggle_off_hides_banner(self):
        Announcement.objects.create(
            message="Grand Festive Healing Discount",
            is_active=True,
        )
        # With toggle on, banner renders
        res1 = self.client.get(reverse("user:home"))
        self.assertContains(res1, "Grand Festive Healing Discount")

        # With toggle off, banner is suppressed
        self.settings.enable_announcement_banner = False
        self.settings.save()

        res2 = self.client.get(reverse("user:home"))
        self.assertNotContains(res2, "Grand Festive Healing Discount")


class ContactFormAndSubmissionTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse("user:contact")
        SiteSettings.load()

    def test_valid_contact_submission_persists_to_database(self):
        initial_count = SupportRequest.objects.count()
        payload = {
            "name": "Geeta Patel",
            "email": "geeta.patel@example.com",
            "phone": "+91 98250 54321",
            "subject": "Demo Request",
            "message": "I would like to schedule a product demonstration at your Ahmedabad experience center.",
        }
        response = self.client.post(self.url, data=payload, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(SupportRequest.objects.count(), initial_count + 1)

        record = SupportRequest.objects.filter(email="geeta.patel@example.com").first()
        self.assertIsNotNone(record)
        self.assertEqual(record.name, "Geeta Patel")
        self.assertEqual(record.phone, "9825054321")
        self.assertEqual(record.request_type, SupportRequest.RequestType.DEMO_REQUEST)
        self.assertEqual(record.status, SupportRequest.Status.NEW)
        self.assertTrue(record.ticket_number.startswith("SR-"))
        self.assertEqual(record.admin_notes, "")

        # Verify confirmation message
        self.assertContains(response, record.ticket_number)

    def test_invalid_contact_submission_creates_no_record(self):
        initial_count = SupportRequest.objects.count()
        # Invalid phone and missing message
        payload = {
            "name": "Invalid Submitter",
            "email": "invalid-email-address",
            "phone": "12345",  # Invalid Indian phone
            "subject": "Other",
            "message": "",
        }
        response = self.client.post(self.url, data=payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(SupportRequest.objects.count(), initial_count)
        self.assertFormError(response.context["form"], "phone", "Please enter a valid 10-digit Indian mobile number (e.g. 98250 12345).")
        self.assertFormError(response.context["form"], "email", "Please enter a valid email address.")

    def test_internal_fields_cannot_be_overridden_via_public_post(self):
        payload = {
            "name": "Security Tester",
            "email": "tester@example.com",
            "phone": "98250 99887",
            "subject": "Other",
            "message": "Testing that internal fields cannot be set by public clients.",
            # Malicious internal status and notes payload
            "status": "closed",
            "admin_notes": "Malicious injected internal note",
            "ticket_number": "SR-CUSTOM-OVERRIDE",
        }
        response = self.client.post(self.url, data=payload, follow=True)
        self.assertEqual(response.status_code, 200)

        record = SupportRequest.objects.filter(email="tester@example.com").first()
        self.assertIsNotNone(record)
        # Status MUST remain NEW and admin_notes MUST remain empty
        self.assertEqual(record.status, SupportRequest.Status.NEW)
        self.assertEqual(record.admin_notes, "")
        self.assertNotEqual(record.ticket_number, "SR-CUSTOM-OVERRIDE")

    def test_duplicate_submission_prevention(self):
        payload = {
            "name": "Ramesh Shah",
            "email": "ramesh@example.com",
            "phone": "98250 11223",
            "subject": "Product Enquiry",
            "message": "Enquiry for spinal decompression bed availability.",
        }
        res1 = self.client.post(self.url, data=payload, follow=True)
        self.assertEqual(res1.status_code, 200)
        self.assertEqual(SupportRequest.objects.filter(phone="9825011223").count(), 1)

        # Immediate duplicate submission
        res2 = self.client.post(self.url, data=payload, follow=True)
        self.assertEqual(res2.status_code, 200)
        # Still exactly 1 record
        self.assertEqual(SupportRequest.objects.filter(phone="9825011223").count(), 1)
        self.assertContains(res2, "already received your message recently")


class SupportTicketFormAndSubmissionTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse("user:support")
        SiteSettings.load()

    def test_valid_support_ticket_persists_to_database(self):
        initial_count = SupportRequest.objects.count()
        payload = {
            "name": "Kavita Desai",
            "email": "kavita@example.com",
            "phone": "+91 98250 88776",
            "product_name": "AyurSpine Belt",
            "message": "The air pump valve seems loose after 6 months of daily traction usage.",
        }
        response = self.client.post(self.url, data=payload, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(SupportRequest.objects.count(), initial_count + 1)

        ticket = SupportRequest.objects.filter(email="kavita@example.com").first()
        self.assertIsNotNone(ticket)
        self.assertEqual(ticket.name, "Kavita Desai")
        self.assertEqual(ticket.product_name, "AyurSpine Belt")
        self.assertEqual(ticket.request_type, SupportRequest.RequestType.PRODUCT_SUPPORT)
        self.assertEqual(ticket.status, SupportRequest.Status.NEW)
        self.assertTrue(ticket.ticket_number.startswith("SR-"))
        self.assertContains(response, ticket.ticket_number)

    def test_invalid_support_ticket_creates_no_record(self):
        initial_count = SupportRequest.objects.count()
        payload = {
            "name": "   ",
            "email": "bad-email",
            "phone": "00000",
            "product_name": "",
            "message": "",
        }
        response = self.client.post(self.url, data=payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(SupportRequest.objects.count(), initial_count)

    def test_duplicate_support_ticket_prevention(self):
        payload = {
            "name": "Mahesh Patel",
            "email": "mahesh@example.com",
            "phone": "98250 66778",
            "product_name": "Kansa Vataki",
            "message": "Need advice on oil formulation for knee joint massage.",
        }
        self.client.post(self.url, data=payload, follow=True)
        self.assertEqual(SupportRequest.objects.filter(phone="9825066778").count(), 1)

        # Immediate duplicate
        res2 = self.client.post(self.url, data=payload, follow=True)
        self.assertEqual(SupportRequest.objects.filter(phone="9825066778").count(), 1)
        self.assertContains(res2, "already received this support ticket recently")





