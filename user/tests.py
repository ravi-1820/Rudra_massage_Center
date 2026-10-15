from django.test import TestCase, Client
from django.urls import reverse
from .models import Category, Service, CustomerNeed, BodyPart, ServiceType, IntendedUse


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
