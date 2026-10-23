from io import BytesIO
from PIL import Image
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase
from django.urls import reverse

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


def create_test_image(filename="test_image.png"):
    file_obj = BytesIO()
    image = Image.new("RGB", (100, 100), color="green")
    image.save(file_obj, format="PNG")
    file_obj.seek(0)
    return SimpleUploadedFile(
        filename,
        file_obj.read(),
        content_type="image/png",
    )


class CustomAdminAuthenticationAndAuthorizationTests(TestCase):
    def setUp(self):
        self.client = Client()

        # Users
        self.staff_user = User.objects.create_user(
            username="staff_member",
            password="StaffPassword123!",
            is_staff=True,
            is_superuser=False,
        )
        self.superuser = User.objects.create_superuser(
            username="admin_super",
            password="SuperPassword123!",
            email="admin@example.com",
        )
        self.customer_user = User.objects.create_user(
            username="normal_customer",
            password="CustomerPassword123!",
            is_staff=False,
            is_superuser=False,
        )

        # Core Admin URLs
        self.dashboard_url = reverse("custom_admin:dashboard")
        self.services_url = reverse("custom_admin:services")
        self.enquiries_url = reverse("custom_admin:enquiries")
        self.appointments_url = reverse("custom_admin:appointments")
        self.offers_url = reverse("custom_admin:offers")
        self.settings_url = reverse("custom_admin:settings")
        self.support_requests_url = reverse("custom_admin:support_requests")
        self.login_url = reverse("custom_admin:login")
        self.logout_url = reverse("custom_admin:logout")

        # Test Data
        self.cat = Category.objects.create(name="Massage Chairs", slug="massage-chairs")
        self.service = Service.objects.create(
            category=self.cat,
            name="Robotic Full Body Recliner",
            slug="robotic-full-body-recliner",
            short_description="Full body 4D robotic massage chair.",
            description="Deep tissue therapy with heated rollers.",
            is_active=True,
        )
        self.enquiry = Enquiry.objects.create(
            name="Rahul Sharma",
            phone="9876543210",
            email="rahul@example.com",
            city="Ahmedabad",
            service=self.service,
            status=Enquiry.Status.NEW,
        )

    # 1. Anonymous Access Tests
    def test_anonymous_users_redirected_to_login(self):
        protected_urls = [
            self.dashboard_url,
            self.services_url,
            self.enquiries_url,
            self.appointments_url,
            self.offers_url,
            self.settings_url,
            self.support_requests_url,
        ]
        for url in protected_urls:
            response = self.client.get(url)
            self.assertEqual(
                response.status_code,
                302,
                f"Anonymous user was not redirected for {url}",
            )
            self.assertIn(self.login_url, response.url)

    # 2. Non-staff User Access Tests
    def test_authenticated_non_staff_users_denied_access(self):
        self.client.login(username="normal_customer", password="CustomerPassword123!")
        protected_urls = [
            self.dashboard_url,
            self.services_url,
            self.enquiries_url,
            self.appointments_url,
            self.offers_url,
            self.settings_url,
            self.support_requests_url,
        ]
        for url in protected_urls:
            response = self.client.get(url)
            self.assertEqual(
                response.status_code,
                403,
                f"Non-staff user was not denied (expected 403) for {url}",
            )

    # 3. Staff / Superuser Access Tests
    def test_staff_user_can_access_all_admin_pages(self):
        self.client.login(username="staff_member", password="StaffPassword123!")
        protected_urls = [
            self.dashboard_url,
            self.services_url,
            self.enquiries_url,
            self.appointments_url,
            self.offers_url,
            self.settings_url,
        ]
        for url in protected_urls:
            response = self.client.get(url)
            self.assertEqual(
                response.status_code,
                200,
                f"Staff user could not access {url}",
            )

    def test_superuser_can_access_all_admin_pages(self):
        self.client.login(username="admin_super", password="SuperPassword123!")
        response = self.client.get(self.dashboard_url)
        self.assertEqual(response.status_code, 200)

    # 4. Custom Admin Login Workflow
    def test_custom_admin_login_page_renders_cleanly(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Admin Portal")
        self.assertContains(response, "Staff Username")

    def test_custom_admin_login_success_staff_redirects_to_dashboard(self):
        response = self.client.post(
            self.login_url,
            {
                "username": "staff_member",
                "password": "StaffPassword123!",
            },
        )
        self.assertRedirects(response, self.dashboard_url)

    def test_custom_admin_login_success_redirects_to_safe_next_url(self):
        response = self.client.post(
            f"{self.login_url}?next={self.services_url}",
            {
                "username": "staff_member",
                "password": "StaffPassword123!",
                "next": self.services_url,
            },
        )
        self.assertRedirects(response, self.services_url)

    def test_custom_admin_login_blocks_malicious_open_redirect(self):
        response = self.client.post(
            f"{self.login_url}?next=https://malicious-site.example.com/exploit",
            {
                "username": "staff_member",
                "password": "StaffPassword123!",
                "next": "https://malicious-site.example.com/exploit",
            },
        )
        self.assertRedirects(response, self.dashboard_url)

    def test_custom_admin_login_non_staff_credentials_rejected(self):
        response = self.client.post(
            self.login_url,
            {
                "username": "normal_customer",
                "password": "CustomerPassword123!",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Access denied")

    def test_custom_admin_login_invalid_password(self):
        response = self.client.post(
            self.login_url,
            {
                "username": "staff_member",
                "password": "WrongPassword999!",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Invalid username or password")

    # 5. Custom Admin Logout Workflow
    def test_custom_admin_logout_requires_post(self):
        self.client.login(username="staff_member", password="StaffPassword123!")
        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, 405)

    def test_custom_admin_logout_post_terminates_session(self):
        self.client.login(username="staff_member", password="StaffPassword123!")
        response = self.client.post(self.logout_url)
        self.assertRedirects(response, self.login_url)

        dash_response = self.client.get(self.dashboard_url)
        self.assertEqual(dash_response.status_code, 302)
        self.assertIn(self.login_url, dash_response.url)

    # 6. Enquiry Status Update Workflow
    def test_staff_can_update_enquiry_status(self):
        self.client.login(username="staff_member", password="StaffPassword123!")
        update_url = reverse(
            "custom_admin:update_enquiry_status",
            kwargs={"enquiry_id": self.enquiry.id},
        )
        response = self.client.post(
            update_url,
            {
                "status": Enquiry.Status.CONTACTED,
                "admin_notes": "Called customer at 11am; interested in home demo.",
            },
        )
        self.assertRedirects(response, self.enquiries_url)
        self.enquiry.refresh_from_db()
        self.assertEqual(self.enquiry.status, Enquiry.Status.CONTACTED)
        self.assertEqual(
            self.enquiry.admin_notes,
            "Called customer at 11am; interested in home demo.",
        )

    def test_enquiry_status_update_requires_staff(self):
        self.client.login(username="normal_customer", password="CustomerPassword123!")
        update_url = reverse(
            "custom_admin:update_enquiry_status",
            kwargs={"enquiry_id": self.enquiry.id},
        )
        response = self.client.post(
            update_url,
            {"status": Enquiry.Status.RESOLVED},
        )
        self.assertEqual(response.status_code, 403)


class ServiceAndCategoryManagementTests(TestCase):
    def setUp(self):
        self.client = Client()

        # Users
        self.staff_user = User.objects.create_user(
            username="staff_editor",
            password="EditorPassword123!",
            is_staff=True,
        )
        self.customer = User.objects.create_user(
            username="regular_visitor",
            password="VisitorPassword123!",
            is_staff=False,
        )

        # Taxonomies
        self.category = Category.objects.create(
            name="Therapy Beds",
            slug="therapy-beds",
            is_active=True,
            display_order=1,
        )
        self.need = CustomerNeed.objects.create(name="Spinal Alignment", slug="spinal-alignment", is_active=True)
        self.body_part = BodyPart.objects.create(name="Full Spine", slug="full-spine", is_active=True)
        self.service_type = ServiceType.objects.create(name="Traction Beds", slug="traction-beds", is_active=True)
        self.intended_use = IntendedUse.objects.create(name="Clinical Center", slug="clinical-center", is_active=True)

        # Service
        self.service = Service.objects.create(
            category=self.category,
            name="Lumbar Traction Unit",
            slug="lumbar-traction-unit",
            short_description="Decompression therapy for spine relief.",
            description="Detailed specifications for automated lumbar traction bed.",
            is_active=True,
            display_order=1,
        )
        self.service.customer_needs.add(self.need)
        self.service.body_parts.add(self.body_part)
        self.service.service_types.add(self.service_type)
        self.service.intended_uses.add(self.intended_use)

        # URLs
        self.services_list_url = reverse("custom_admin:services")
        self.service_create_url = reverse("custom_admin:service_create")
        self.service_edit_url = reverse("custom_admin:service_edit", kwargs={"service_id": self.service.id})
        self.service_toggle_url = reverse("custom_admin:service_toggle_active", kwargs={"service_id": self.service.id})

        self.categories_list_url = reverse("custom_admin:categories")
        self.category_create_url = reverse("custom_admin:category_create")
        self.category_edit_url = reverse("custom_admin:category_edit", kwargs={"category_id": self.category.id})
        self.category_toggle_url = reverse("custom_admin:category_toggle_active", kwargs={"category_id": self.category.id})

    # Authorization
    def test_anonymous_redirected_from_management_endpoints(self):
        urls = [
            self.service_create_url,
            self.service_edit_url,
            self.categories_list_url,
            self.category_create_url,
            self.category_edit_url,
        ]
        login_url = reverse("custom_admin:login")
        for url in urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 302)
            self.assertIn(login_url, response.url)

    def test_non_staff_denied_from_management_endpoints(self):
        self.client.login(username="regular_visitor", password="VisitorPassword123!")
        urls = [
            self.services_list_url,
            self.service_create_url,
            self.service_edit_url,
            self.categories_list_url,
            self.category_create_url,
            self.category_edit_url,
        ]
        for url in urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 403)

    # Services Management
    def test_staff_can_view_services_with_search_and_filters(self):
        self.client.login(username="staff_editor", password="EditorPassword123!")
        response = self.client.get(self.services_list_url, {"q": "Lumbar"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Lumbar Traction Unit")
        self.assertContains(response, "Therapy Beds")

    def test_staff_create_service_with_image_and_relationships(self):
        self.client.login(username="staff_editor", password="EditorPassword123!")
        test_img = create_test_image("new_bed.png")

        post_data = {
            "name": "Cervical Decompression Cradle",
            "slug": "cervical-decompression-cradle",
            "category": self.category.id,
            "short_description": "Targeted neck and upper spine tension release.",
            "description": "Comprehensive cervical vertebrae decompression device with pneumatic control.",
            "image": test_img,
            "benefits": "Alleviates neck pain and promotes blood flow.",
            "usage_instructions": "Lie flat and adjust pneumatic pump for 15 minutes.",
            "precautions": "Consult doctor if recovering from acute neck fracture.",
            "display_order": 2,
            "is_active": True,
            "is_featured": True,
            "customer_needs": [self.need.id],
            "body_parts": [self.body_part.id],
            "service_types": [self.service_type.id],
            "intended_uses": [self.intended_use.id],
        }

        response = self.client.post(self.service_create_url, post_data)
        self.assertRedirects(response, self.services_list_url)

        new_svc = Service.objects.get(slug="cervical-decompression-cradle")
        self.assertEqual(new_svc.name, "Cervical Decompression Cradle")
        self.assertEqual(new_svc.category, self.category)
        self.assertTrue(new_svc.is_featured)
        self.assertTrue(new_svc.is_active)
        self.assertIn(self.need, new_svc.customer_needs.all())
        self.assertIn(self.body_part, new_svc.body_parts.all())
        self.assertTrue(bool(new_svc.image))

    def test_staff_edit_service(self):
        self.client.login(username="staff_editor", password="EditorPassword123!")
        edit_data = {
            "name": "Advanced Lumbar Traction Bed v2",
            "slug": "lumbar-traction-unit",
            "category": self.category.id,
            "short_description": "Updated decompression description.",
            "description": "Updated full clinical description.",
            "display_order": 5,
            "is_active": True,
        }
        response = self.client.post(self.service_edit_url, edit_data)
        self.assertRedirects(response, self.services_list_url)

        self.service.refresh_from_db()
        self.assertEqual(self.service.name, "Advanced Lumbar Traction Bed v2")
        self.assertEqual(self.service.display_order, 5)

    def test_staff_toggle_service_active_status(self):
        self.client.login(username="staff_editor", password="EditorPassword123!")
        self.assertTrue(self.service.is_active)

        # Deactivate
        response = self.client.post(self.service_toggle_url)
        self.assertRedirects(response, self.services_list_url)
        self.service.refresh_from_db()
        self.assertFalse(self.service.is_active)

        # Reactivate
        response = self.client.post(self.service_toggle_url)
        self.assertRedirects(response, self.services_list_url)
        self.service.refresh_from_db()
        self.assertTrue(self.service.is_active)

    def test_service_validation_errors(self):
        self.client.login(username="staff_editor", password="EditorPassword123!")
        # Missing required name and category
        response = self.client.post(self.service_create_url, {
            "name": "   ",
            "short_description": "Only whitespace",
        })
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response.context["form"], "name", "This field is required.")
        self.assertFormError(response.context["form"], "category", "This field is required.")

    # Categories Management
    def test_staff_can_view_categories_list(self):
        self.client.login(username="staff_editor", password="EditorPassword123!")
        response = self.client.get(self.categories_list_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Therapy Beds")
        self.assertContains(response, "1 solution")

    def test_staff_create_category_with_image(self):
        self.client.login(username="staff_editor", password="EditorPassword123!")
        test_img = create_test_image("kansa.png")

        post_data = {
            "name": "Kansa Wand Devices",
            "slug": "kansa-wand-devices",
            "description": "Traditional Vedic bronze foot and face rejuvenation tools.",
            "image": test_img,
            "display_order": 3,
            "is_active": True,
        }
        response = self.client.post(self.category_create_url, post_data)
        self.assertRedirects(response, self.categories_list_url)

        new_cat = Category.objects.get(slug="kansa-wand-devices")
        self.assertEqual(new_cat.name, "Kansa Wand Devices")
        self.assertTrue(bool(new_cat.image))

    def test_staff_edit_category(self):
        self.client.login(username="staff_editor", password="EditorPassword123!")
        edit_data = {
            "name": "Orthopedic Therapy Beds",
            "slug": "therapy-beds",
            "description": "Updated medical decompression equipment.",
            "display_order": 10,
            "is_active": True,
        }
        response = self.client.post(self.category_edit_url, edit_data)
        self.assertRedirects(response, self.categories_list_url)

        self.category.refresh_from_db()
        self.assertEqual(self.category.name, "Orthopedic Therapy Beds")
        self.assertEqual(self.category.display_order, 10)

    def test_staff_toggle_category_active_status(self):
        self.client.login(username="staff_editor", password="EditorPassword123!")
        self.assertTrue(self.category.is_active)

        # Deactivate
        response = self.client.post(self.category_toggle_url)
        self.assertRedirects(response, self.categories_list_url)
        self.category.refresh_from_db()
        self.assertFalse(self.category.is_active)

    def test_category_validation_duplicate_name(self):
        self.client.login(username="staff_editor", password="EditorPassword123!")
        response = self.client.post(self.category_create_url, {
            "name": "Therapy Beds",
        })
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response.context["form"], "name", "A category with this name already exists.")

    # Public Integration
    def test_public_website_reflects_service_and_category_updates(self):
        public_services_url = reverse("user:services")
        detail_url = reverse("user:service_detail", kwargs={"slug": self.service.slug})

        # When active, it displays on public site
        response = self.client.get(public_services_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.service.name)

        detail_response = self.client.get(detail_url)
        self.assertEqual(detail_response.status_code, 200)
        self.assertContains(detail_response, self.service.name)

        # When deactivated via admin, it disappears from public listing and returns 404 on detail
        self.service.is_active = False
        self.service.save()

        response_inactive = self.client.get(public_services_url)
        self.assertNotContains(response_inactive, self.service.name)

        detail_inactive = self.client.get(detail_url)
        self.assertEqual(detail_inactive.status_code, 404)


class AdminEnquiriesManagementTests(TestCase):
    def setUp(self):
        self.client = Client()

        # Users
        self.staff_user = User.objects.create_user(
            username="enquiry_lead_staff",
            password="LeadPassword123!",
            is_staff=True,
        )
        self.customer = User.objects.create_user(
            username="regular_visitor_user",
            password="VisitorPassword123!",
            is_staff=False,
        )

        # Category & Services
        self.category = Category.objects.create(name="Spine Therapy", slug="spine-therapy", is_active=True)
        self.service1 = Service.objects.create(
            category=self.category,
            name="Lumbar Traction Machine",
            slug="lumbar-traction-machine",
            short_description="Spine relief.",
            description="Lumbar traction bed for clinical decompression.",
            is_active=True,
        )
        self.service2 = Service.objects.create(
            category=self.category,
            name="Cervical Relaxation Collar",
            slug="cervical-relaxation-collar",
            short_description="Neck tension relief.",
            description="Pneumatic neck traction collar.",
            is_active=True,
        )

        # Enquiries
        self.enquiry1 = Enquiry.objects.create(
            name="Pooja Mehta",
            phone="9825011111",
            email="pooja.m@example.com",
            city="Ahmedabad",
            service=self.service1,
            usage_intention=Enquiry.UsageIntention.PERSONAL,
            callback_time=Enquiry.CallbackTime.MORNING,
            message="Interested in testing the lumbar traction bed for lower back disc pain.",
            status=Enquiry.Status.NEW,
        )
        self.enquiry2 = Enquiry.objects.create(
            name="Suresh Patel",
            phone="9898022222",
            email="suresh.p@example.com",
            city="Surat",
            service=self.service2,
            usage_intention=Enquiry.UsageIntention.CLINIC,
            callback_time=Enquiry.CallbackTime.EVENING,
            message="Looking for clinic trial demo units.",
            status=Enquiry.Status.IN_DISCUSSION,
            admin_notes="Called once on Monday; sent product catalog PDF.",
        )
        self.enquiry3 = Enquiry.objects.create(
            name="Dr. Hiren Joshi",
            phone="9727033333",
            email="hiren.j@example.com",
            city="Vadodara",
            service=None,
            service_name_snapshot="General Wellness Consultation",
            status=Enquiry.Status.RESOLVED,
            admin_notes="Delivered unit and confirmed installation.",
        )

        # URLs
        self.enquiries_list_url = reverse("custom_admin:enquiries")
        self.enquiry1_detail_url = reverse("custom_admin:enquiry_detail", kwargs={"enquiry_id": self.enquiry1.id})
        self.enquiry1_status_url = reverse("custom_admin:update_enquiry_status", kwargs={"enquiry_id": self.enquiry1.id})
        self.public_enquiry_url = reverse("user:enquiry")

    # 1. Authorization
    def test_anonymous_user_redirected_from_enquiry_management(self):
        login_url = reverse("custom_admin:login")

        res_list = self.client.get(self.enquiries_list_url)
        self.assertEqual(res_list.status_code, 302)
        self.assertIn(login_url, res_list.url)

        res_detail = self.client.get(self.enquiry1_detail_url)
        self.assertEqual(res_detail.status_code, 302)
        self.assertIn(login_url, res_detail.url)

        res_status = self.client.post(self.enquiry1_status_url, {"status": Enquiry.Status.CONTACTED})
        self.assertEqual(res_status.status_code, 302)
        self.assertIn(login_url, res_status.url)

    def test_non_staff_user_denied_from_enquiry_management(self):
        self.client.login(username="regular_visitor_user", password="VisitorPassword123!")

        res_list = self.client.get(self.enquiries_list_url)
        self.assertEqual(res_list.status_code, 403)

        res_detail = self.client.get(self.enquiry1_detail_url)
        self.assertEqual(res_detail.status_code, 403)

        res_status = self.client.post(self.enquiry1_status_url, {"status": Enquiry.Status.CONTACTED})
        self.assertEqual(res_status.status_code, 403)

    # 2. Staff View, Search & Filtering
    def test_staff_can_view_enquiries_list_and_metrics(self):
        self.client.login(username="enquiry_lead_staff", password="LeadPassword123!")
        response = self.client.get(self.enquiries_list_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Pooja Mehta")
        self.assertContains(response, "Suresh Patel")
        self.assertContains(response, "Dr. Hiren Joshi")
        self.assertContains(response, "Lumbar Traction Machine")

    def test_staff_search_enquiry_by_name_phone_email_city(self):
        self.client.login(username="enquiry_lead_staff", password="LeadPassword123!")

        # Search by customer name
        res_name = self.client.get(self.enquiries_list_url, {"q": "Pooja"})
        self.assertEqual(res_name.status_code, 200)
        self.assertContains(res_name, "Pooja Mehta")
        self.assertNotContains(res_name, "Suresh Patel")

        # Search by phone
        res_phone = self.client.get(self.enquiries_list_url, {"q": "9898022222"})
        self.assertEqual(res_phone.status_code, 200)
        self.assertContains(res_phone, "Suresh Patel")
        self.assertNotContains(res_phone, "Pooja Mehta")

        # Search by city
        res_city = self.client.get(self.enquiries_list_url, {"q": "Vadodara"})
        self.assertEqual(res_city.status_code, 200)
        self.assertContains(res_city, "Dr. Hiren Joshi")
        self.assertNotContains(res_city, "Pooja Mehta")

    def test_staff_filter_enquiry_by_status(self):
        self.client.login(username="enquiry_lead_staff", password="LeadPassword123!")

        res_new = self.client.get(self.enquiries_list_url, {"status": Enquiry.Status.NEW})
        self.assertEqual(res_new.status_code, 200)
        self.assertContains(res_new, "Pooja Mehta")
        self.assertNotContains(res_new, "Suresh Patel")
        self.assertNotContains(res_new, "Dr. Hiren Joshi")

        res_resolved = self.client.get(self.enquiries_list_url, {"status": Enquiry.Status.RESOLVED})
        self.assertEqual(res_resolved.status_code, 200)
        self.assertContains(res_resolved, "Dr. Hiren Joshi")
        self.assertNotContains(res_resolved, "Pooja Mehta")

    def test_staff_filter_enquiry_by_service(self):
        self.client.login(username="enquiry_lead_staff", password="LeadPassword123!")
        response = self.client.get(self.enquiries_list_url, {"service": self.service1.id})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Pooja Mehta")
        self.assertNotContains(response, "Suresh Patel")

    def test_staff_filter_enquiry_by_date_range(self):
        self.client.login(username="enquiry_lead_staff", password="LeadPassword123!")
        response = self.client.get(self.enquiries_list_url, {"date_range": "today"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Pooja Mehta")

    # 3. Enquiry Detail & Follow-Up Workflow
    def test_staff_can_view_enquiry_detail_page(self):
        self.client.login(username="enquiry_lead_staff", password="LeadPassword123!")
        response = self.client.get(self.enquiry1_detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Pooja Mehta")
        self.assertContains(response, "9825011111")
        self.assertContains(response, "pooja.m@example.com")
        self.assertContains(response, "Ahmedabad")
        self.assertContains(response, "Lumbar Traction Machine")
        self.assertContains(response, "Interested in testing the lumbar traction bed")

    def test_staff_can_update_status_and_notes_via_detail_view(self):
        self.client.login(username="enquiry_lead_staff", password="LeadPassword123!")
        post_data = {
            "status": Enquiry.Status.CONTACTED,
            "admin_notes": "Spoke to customer at 10:30am; agreed to schedule a home demonstration next week.",
        }
        response = self.client.post(self.enquiry1_detail_url, post_data)
        self.assertRedirects(response, self.enquiries_list_url)

        self.enquiry1.refresh_from_db()
        self.assertEqual(self.enquiry1.status, Enquiry.Status.CONTACTED)
        self.assertEqual(
            self.enquiry1.admin_notes,
            "Spoke to customer at 10:30am; agreed to schedule a home demonstration next week.",
        )

    def test_staff_inline_status_update_endpoint(self):
        self.client.login(username="enquiry_lead_staff", password="LeadPassword123!")
        response = self.client.post(self.enquiry1_status_url, {
            "status": Enquiry.Status.RESOLVED,
            "admin_notes": "Closed after successful clinic trial.",
        })
        self.assertRedirects(response, self.enquiries_list_url)

        self.enquiry1.refresh_from_db()
        self.assertEqual(self.enquiry1.status, Enquiry.Status.RESOLVED)
        self.assertEqual(self.enquiry1.admin_notes, "Closed after successful clinic trial.")

    def test_invalid_status_value_rejected(self):
        self.client.login(username="enquiry_lead_staff", password="LeadPassword123!")

        # Via inline endpoint
        response_inline = self.client.post(self.enquiry1_status_url, {"status": "fraud_status"})
        self.assertRedirects(response_inline, self.enquiries_list_url)
        self.enquiry1.refresh_from_db()
        self.assertEqual(self.enquiry1.status, Enquiry.Status.NEW)

        # Via detail view form
        response_form = self.client.post(self.enquiry1_detail_url, {"status": "fraud_status"})
        self.assertEqual(response_form.status_code, 200)
        self.assertFormError(
            response_form.context["form"],
            "status",
            "Select a valid choice. fraud_status is not one of the available choices.",
        )

    # 4. Public Enquiry Submission Integration
    def test_public_enquiry_submission_persists_to_database(self):
        public_post_data = {
            "name": "Kavita Shah",
            "phone": "98250 99999",
            "email": "kavita.shah@example.com",
            "city": "Gandhinagar",
            "service": self.service1.id,
            "usage_intention": Enquiry.UsageIntention.PERSONAL,
            "callback_time": Enquiry.CallbackTime.MORNING,
            "message": "Please call me regarding dimensions and electrical requirements.",
        }
        response = self.client.post(self.public_enquiry_url, public_post_data)
        self.assertRedirects(response, self.public_enquiry_url)

        created_enq = Enquiry.objects.get(email="kavita.shah@example.com")
        self.assertEqual(created_enq.name, "Kavita Shah")
        self.assertEqual(created_enq.phone, "9825099999")
        self.assertEqual(created_enq.city, "Gandhinagar")
        self.assertEqual(created_enq.service, self.service1)
        self.assertEqual(created_enq.status, Enquiry.Status.NEW)

        # Confirm staff can see this new submission in admin
        self.client.login(username="enquiry_lead_staff", password="LeadPassword123!")
        admin_response = self.client.get(self.enquiries_list_url)
        self.assertContains(admin_response, "Kavita Shah")


class AdminAppointmentsManagementTests(TestCase):
    def setUp(self):
        self.client = Client()

        self.staff_user = User.objects.create_user(
            username="apt_staff_mgr",
            password="AptStaffPass123!",
            is_staff=True,
        )
        self.non_staff_user = User.objects.create_user(
            username="regular_visitor",
            password="VisitorPass123!",
            is_staff=False,
        )

        self.category = Category.objects.create(name="Ayurvedic Chairs", slug="ayurvedic-chairs", is_active=True)
        self.service1 = Service.objects.create(
            category=self.category,
            name="Rudra Full Body Decompression",
            slug="rudra-full-body-decompression",
            short_description="Full body motorized decompression therapy.",
            description="Deep tissue decompression machine.",
            is_active=True,
        )
        self.service2 = Service.objects.create(
            category=self.category,
            name="Cervical Spine Massager",
            slug="cervical-spine-massager",
            short_description="Targeted neck and shoulder soothing therapy.",
            description="Ergonomic neck support with thermal rollers.",
            is_active=True,
        )

        from datetime import date, timedelta
        self.today = date.today()
        self.tomorrow = self.today + timedelta(days=1)
        self.yesterday = self.today - timedelta(days=1)

        self.apt1 = Appointment.objects.create(
            booking_reference="APT-901",
            name="Nilesh Patel",
            phone="9825123456",
            email="nilesh@example.com",
            city="Ahmedabad",
            service=self.service1,
            service_name_snapshot=self.service1.name,
            appointment_date=self.tomorrow,
            time_slot="morning",
            demo_format="store",
            notes="Please keep chair ready for trial.",
            status=Appointment.Status.PENDING,
        )
        self.apt2 = Appointment.objects.create(
            booking_reference="APT-902",
            name="Meera Joshi",
            phone="9876543210",
            email="meera@example.com",
            city="Surat",
            service=self.service2,
            service_name_snapshot=self.service2.name,
            appointment_date=self.yesterday,
            time_slot="afternoon",
            demo_format="home",
            notes="Home trial requested.",
            status=Appointment.Status.CONFIRMED,
        )
        self.apt3 = Appointment.objects.create(
            booking_reference="APT-903",
            name="Rajesh Dave",
            phone="9898011223",
            email="rajesh@example.com",
            city="Vadodara",
            service=self.service1,
            service_name_snapshot=self.service1.name,
            appointment_date=self.today,
            time_slot="midday",
            demo_format="store",
            notes="Clinic demo.",
            status=Appointment.Status.COMPLETED,
        )

        self.appointments_url = reverse("custom_admin:appointments")
        self.apt1_detail_url = reverse("custom_admin:appointment_detail", kwargs={"appointment_id": self.apt1.id})
        self.apt1_status_url = reverse("custom_admin:update_appointment_status", kwargs={"appointment_id": self.apt1.id})
        self.login_url = reverse("custom_admin:login")

    def test_anonymous_access_redirects_to_login(self):
        for url in [self.appointments_url, self.apt1_detail_url, self.apt1_status_url]:
            res = self.client.get(url)
            self.assertEqual(res.status_code, 302)
            self.assertIn(self.login_url, res.url)

    def test_non_staff_access_denied_403(self):
        self.client.login(username="regular_visitor", password="VisitorPass123!")
        for url in [self.appointments_url, self.apt1_detail_url]:
            res = self.client.get(url)
            self.assertEqual(res.status_code, 403)

    def test_staff_can_list_and_view_counters(self):
        self.client.login(username="apt_staff_mgr", password="AptStaffPass123!")
        res = self.client.get(self.appointments_url)
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "APT-901")
        self.assertContains(res, "Nilesh Patel")
        self.assertContains(res, "APT-902")
        self.assertContains(res, "Meera Joshi")
        self.assertContains(res, "APT-903")
        self.assertEqual(res.context["total_count"], Appointment.objects.count())
        self.assertEqual(res.context["pending_count"], Appointment.objects.filter(status=Appointment.Status.PENDING).count())
        self.assertEqual(res.context["confirmed_count"], Appointment.objects.filter(status=Appointment.Status.CONFIRMED).count())
        self.assertEqual(res.context["completed_count"], Appointment.objects.filter(status=Appointment.Status.COMPLETED).count())

    def test_search_appointments(self):
        self.client.login(username="apt_staff_mgr", password="AptStaffPass123!")

        # Search by customer name
        res_name = self.client.get(f"{self.appointments_url}?q=Nilesh")
        self.assertEqual(res_name.status_code, 200)
        self.assertContains(res_name, "Nilesh Patel")
        self.assertNotContains(res_name, "Meera Joshi")

        # Search by booking reference
        res_ref = self.client.get(f"{self.appointments_url}?q=APT-902")
        self.assertEqual(res_ref.status_code, 200)
        self.assertContains(res_ref, "Meera Joshi")
        self.assertNotContains(res_ref, "Nilesh Patel")

        # Search by phone
        res_phone = self.client.get(f"{self.appointments_url}?q=9898011223")
        self.assertEqual(res_phone.status_code, 200)
        self.assertContains(res_phone, "Rajesh Dave")
        self.assertNotContains(res_phone, "Nilesh Patel")

    def test_filter_appointments_by_status_and_service(self):
        self.client.login(username="apt_staff_mgr", password="AptStaffPass123!")

        # Filter by status: pending
        res_status = self.client.get(f"{self.appointments_url}?status=pending")
        self.assertEqual(res_status.status_code, 200)
        self.assertContains(res_status, "APT-901")
        self.assertNotContains(res_status, "APT-902")
        self.assertNotContains(res_status, "APT-903")

        # Filter by service: service2
        res_service = self.client.get(f"{self.appointments_url}?service={self.service2.id}")
        self.assertEqual(res_service.status_code, 200)
        self.assertContains(res_service, "Meera Joshi")
        self.assertNotContains(res_service, "Nilesh Patel")

    def test_filter_appointments_by_date_range(self):
        self.client.login(username="apt_staff_mgr", password="AptStaffPass123!")

        # Filter today
        res_today = self.client.get(f"{self.appointments_url}?date_range=today")
        self.assertEqual(res_today.status_code, 200)
        self.assertContains(res_today, "APT-903")
        self.assertNotContains(res_today, "APT-901")

        # Filter past
        res_past = self.client.get(f"{self.appointments_url}?date_range=past")
        self.assertEqual(res_past.status_code, 200)
        self.assertContains(res_past, "APT-902")
        self.assertNotContains(res_past, "APT-901")

        # Filter upcoming
        res_upcoming = self.client.get(f"{self.appointments_url}?date_range=upcoming")
        self.assertEqual(res_upcoming.status_code, 200)
        self.assertContains(res_upcoming, "APT-901")
        self.assertContains(res_upcoming, "APT-903")
        self.assertNotContains(res_upcoming, "APT-902")

    def test_view_appointment_detail_page(self):
        self.client.login(username="apt_staff_mgr", password="AptStaffPass123!")
        res = self.client.get(self.apt1_detail_url)
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "APT-901")
        self.assertContains(res, "Nilesh Patel")
        self.assertContains(res, "9825123456")
        self.assertContains(res, "nilesh@example.com")
        self.assertContains(res, "Rudra Full Body Decompression")
        self.assertContains(res, "Please keep chair ready for trial.")

    def test_staff_can_update_status_and_notes_via_detail_view(self):
        self.client.login(username="apt_staff_mgr", password="AptStaffPass123!")
        post_data = {
            "status": Appointment.Status.CONFIRMED,
            "admin_notes": "Client confirmed via phone. Assigned demo kit #2.",
        }
        res = self.client.post(self.apt1_detail_url, post_data)
        self.assertRedirects(res, self.appointments_url)

        self.apt1.refresh_from_db()
        self.assertEqual(self.apt1.status, Appointment.Status.CONFIRMED)
        self.assertEqual(self.apt1.admin_notes, "Client confirmed via phone. Assigned demo kit #2.")

    def test_staff_inline_status_update_endpoint(self):
        self.client.login(username="apt_staff_mgr", password="AptStaffPass123!")
        res = self.client.post(self.apt1_status_url, {
            "status": Appointment.Status.COMPLETED,
            "admin_notes": "Trial successfully concluded at the centre.",
        })
        self.assertRedirects(res, self.appointments_url)

        self.apt1.refresh_from_db()
        self.assertEqual(self.apt1.status, Appointment.Status.COMPLETED)
        self.assertEqual(self.apt1.admin_notes, "Trial successfully concluded at the centre.")

    def test_staff_update_status_via_list_post(self):
        self.client.login(username="apt_staff_mgr", password="AptStaffPass123!")
        res = self.client.post(self.appointments_url, {
            "appointment_id": self.apt1.id,
            "status": Appointment.Status.CANCELLED,
            "admin_notes": "Client requested cancellation due to travel.",
        })
        self.assertRedirects(res, self.appointments_url)

        self.apt1.refresh_from_db()
        self.assertEqual(self.apt1.status, Appointment.Status.CANCELLED)
        self.assertEqual(self.apt1.admin_notes, "Client requested cancellation due to travel.")

    def test_invalid_status_value_rejected(self):
        self.client.login(username="apt_staff_mgr", password="AptStaffPass123!")

        # Via inline endpoint
        res_inline = self.client.post(self.apt1_status_url, {"status": "unrecognized_status"})
        self.assertRedirects(res_inline, self.appointments_url)
        self.apt1.refresh_from_db()
        self.assertEqual(self.apt1.status, Appointment.Status.PENDING)

        # Via detail view form
        res_form = self.client.post(self.apt1_detail_url, {"status": "unrecognized_status"})
        self.assertEqual(res_form.status_code, 200)
        self.assertFormError(
            res_form.context["form"],
            "status",
            "Select a valid choice. unrecognized_status is not one of the available choices.",
        )


class CustomAdminSiteSettingsManagementTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.staff_user = User.objects.create_user(
            username="settings_staff",
            password="StaffPass123!",
            is_staff=True,
        )
        self.url = reverse("custom_admin:settings")
        SiteSettings.objects.all().delete()
        self.settings = SiteSettings.objects.create(
            pk=1,
            business_name="Rudra Therapy Core",
            primary_phone="+91 98250 11111",
            contact_email="care@rudracore.com",
            whatsapp_number="+91 98250 11111",
            business_address="Bodakdev, Ahmedabad",
            google_maps_url="https://maps.google.com/?q=RudraAhmedabad",
            business_hours="Mon - Sat: 9:00 AM - 7:00 PM",
            enable_announcement_banner=True,
            enable_whatsapp_floating=True,
        )

    def test_settings_get_renders_existing_values(self):
        self.client.login(username="settings_staff", password="StaffPass123!")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Rudra Therapy Core")
        self.assertContains(response, "+91 98250 11111")
        self.assertContains(response, "care@rudracore.com")
        self.assertContains(response, "Bodakdev, Ahmedabad")

    def test_settings_post_valid_updates_database(self):
        self.client.login(username="settings_staff", password="StaffPass123!")
        payload = {
            "business_name": "Rudra Wellness & Therapy Sanctuary",
            "primary_phone": "+91 98250 99999",
            "contact_email": "hello@rudrasanctuary.com",
            "whatsapp_number": "+91 98250 88888",
            "business_address": "Suite 501, SG Highway, Bodakdev, Ahmedabad 380054",
            "google_maps_url": "https://maps.google.com/?q=NewLocation",
            "business_hours": "Mon - Sun: 8:00 AM - 9:00 PM",
            "enable_announcement_banner": "on",
            "enable_whatsapp_floating": "on",
        }
        response = self.client.post(self.url, data=payload, follow=True)
        self.assertEqual(response.status_code, 200)

        # Confirm database has been updated
        self.settings.refresh_from_db()
        self.assertEqual(self.settings.business_name, "Rudra Wellness & Therapy Sanctuary")
        self.assertEqual(self.settings.primary_phone, "+91 98250 99999")
        self.assertEqual(self.settings.contact_email, "hello@rudrasanctuary.com")
        self.assertEqual(self.settings.whatsapp_number, "+91 98250 88888")
        self.assertEqual(self.settings.business_address, "Suite 501, SG Highway, Bodakdev, Ahmedabad 380054")
        self.assertTrue(self.settings.enable_announcement_banner)
        self.assertTrue(self.settings.enable_whatsapp_floating)
        # Singleton count remains 1
        self.assertEqual(SiteSettings.objects.count(), 1)

    def test_settings_post_invalid_validation_failure(self):
        self.client.login(username="settings_staff", password="StaffPass123!")
        payload = {
            "business_name": "   ",  # Blank whitespace
            "primary_phone": "",
            "contact_email": "not-an-email",
            "whatsapp_number": "+91 98250 00000",
            "business_address": "",
        }
        response = self.client.post(self.url, data=payload)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response.context["form"], "business_name", "Business name cannot be only whitespace.")
        self.assertFormError(response.context["form"], "contact_email", "Enter a valid email address.")

        # Database record should remain unchanged
        self.settings.refresh_from_db()
        self.assertEqual(self.settings.business_name, "Rudra Therapy Core")


class CustomAdminSupportRequestManagementTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.staff_user = User.objects.create_user(
            username="support_admin",
            password="AdminPassword123!",
            is_staff=True,
        )
        self.list_url = reverse("custom_admin:support_requests")

        # Create test tickets
        self.req1 = SupportRequest.objects.create(
            ticket_number="SR-20261023-AAA111",
            name="Aarav Sharma",
            email="aarav@example.com",
            phone="9825012345",
            request_type=SupportRequest.RequestType.PRODUCT_SUPPORT,
            subject="AyurSpine Belt Support",
            product_name="AyurSpine Belt",
            message="Pump pressure not holding.",
            status=SupportRequest.Status.NEW,
        )
        self.req2 = SupportRequest.objects.create(
            ticket_number="SR-20261023-BBB222",
            name="Bhavna Vora",
            email="bhavna@example.com",
            phone="9825098765",
            request_type=SupportRequest.RequestType.DEMO_REQUEST,
            subject="Demo Request",
            message="Requesting doorstep demo for knee massager.",
            status=SupportRequest.Status.IN_PROGRESS,
            admin_notes="Scheduled demo call on Monday morning.",
        )
        self.req1_detail_url = reverse("custom_admin:support_request_detail", args=[self.req1.id])
        self.req1_status_url = reverse("custom_admin:update_support_request_status", args=[self.req1.id])

    def test_list_view_and_metrics(self):
        self.client.login(username="support_admin", password="AdminPassword123!")
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "SR-20261023-AAA111")
        self.assertContains(response, "SR-20261023-BBB222")
        self.assertContains(response, "Aarav Sharma")
        self.assertContains(response, "Bhavna Vora")
        self.assertEqual(response.context["total_count"], 2)
        self.assertEqual(response.context["new_count"], 1)
        self.assertEqual(response.context["in_progress_count"], 1)

    def test_search_and_filters(self):
        self.client.login(username="support_admin", password="AdminPassword123!")

        # Search query by name
        res_search = self.client.get(f"{self.list_url}?q=Aarav")
        self.assertContains(res_search, "SR-20261023-AAA111")
        self.assertNotContains(res_search, "SR-20261023-BBB222")

        # Search query by ticket number
        res_ticket = self.client.get(f"{self.list_url}?q=BBB222")
        self.assertContains(res_ticket, "SR-20261023-BBB222")
        self.assertNotContains(res_ticket, "SR-20261023-AAA111")

        # Filter by status
        res_status = self.client.get(f"{self.list_url}?status=in_progress")
        self.assertContains(res_status, "Bhavna Vora")
        self.assertNotContains(res_status, "Aarav Sharma")

        # Filter by request type
        res_type = self.client.get(f"{self.list_url}?type=product_support")
        self.assertContains(res_type, "Aarav Sharma")
        self.assertNotContains(res_type, "Bhavna Vora")

    def test_empty_state_rendering(self):
        self.client.login(username="support_admin", password="AdminPassword123!")
        res = self.client.get(f"{self.list_url}?q=NonExistentKeywordXYZ")
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "No Support Requests Found")

    def test_detail_view_renders_ticket_details(self):
        self.client.login(username="support_admin", password="AdminPassword123!")
        response = self.client.get(self.req1_detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "SR-20261023-AAA111")
        self.assertContains(response, "Aarav Sharma")
        self.assertContains(response, "aarav@example.com")
        self.assertContains(response, "9825012345")
        self.assertContains(response, "Pump pressure not holding.")

    def test_detail_view_post_updates_status_and_notes(self):
        self.client.login(username="support_admin", password="AdminPassword123!")
        payload = {
            "status": "resolved",
            "admin_notes": "Replacement air pump dispatched via BlueDart courier.",
        }
        response = self.client.post(self.req1_detail_url, data=payload, follow=True)
        self.assertEqual(response.status_code, 200)

        self.req1.refresh_from_db()
        self.assertEqual(self.req1.status, SupportRequest.Status.RESOLVED)
        self.assertEqual(self.req1.admin_notes, "Replacement air pump dispatched via BlueDart courier.")

    def test_post_only_mutation_endpoint_rejects_get(self):
        self.client.login(username="support_admin", password="AdminPassword123!")
        response = self.client.get(self.req1_status_url)
        # require_POST returns 405 Method Not Allowed
        self.assertEqual(response.status_code, 405)

    def test_post_only_mutation_endpoint_updates_status(self):
        self.client.login(username="support_admin", password="AdminPassword123!")
        payload = {
            "status": "in_progress",
            "admin_notes": "Technician contacted customer to diagnose valve seal.",
        }
        response = self.client.post(self.req1_status_url, data=payload, follow=True)
        self.assertEqual(response.status_code, 200)

        self.req1.refresh_from_db()
        self.assertEqual(self.req1.status, SupportRequest.Status.IN_PROGRESS)
        self.assertEqual(self.req1.admin_notes, "Technician contacted customer to diagnose valve seal.")

    def test_mutation_endpoint_rejects_invalid_status_choice(self):
        self.client.login(username="support_admin", password="AdminPassword123!")
        payload = {
            "status": "hacked_status",
            "admin_notes": "Should not be applied.",
        }
        response = self.client.post(self.req1_status_url, data=payload, follow=True)
        self.assertEqual(response.status_code, 200)

        self.req1.refresh_from_db()
        # Status should NOT change to invalid value
        self.assertEqual(self.req1.status, SupportRequest.Status.NEW)


