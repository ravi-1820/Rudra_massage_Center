from django.urls import path
from . import views

app_name = 'custom_admin'

urlpatterns = [
    # Auth endpoints
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Dashboard
    path('', views.dashboard, name='dashboard'),

    # Services Management
    path('services/', views.services, name='services'),
    path('services/add/', views.service_create, name='service_create'),
    path('services/<int:service_id>/edit/', views.service_edit, name='service_edit'),
    path('services/<int:service_id>/toggle-active/', views.service_toggle_active, name='service_toggle_active'),
    path('services/<int:service_id>/delete/', views.service_delete, name='service_delete'),

    # Categories Management
    path('categories/', views.categories, name='categories'),
    path('categories/add/', views.category_create, name='category_create'),
    path('categories/<int:category_id>/edit/', views.category_edit, name='category_edit'),
    path('categories/<int:category_id>/toggle-active/', views.category_toggle_active, name='category_toggle_active'),
    path('categories/<int:category_id>/delete/', views.category_delete, name='category_delete'),

    # Enquiries
    path('enquiries/', views.enquiries, name='enquiries'),
    path('enquiries/<int:enquiry_id>/', views.enquiry_detail, name='enquiry_detail'),
    path('enquiries/<int:enquiry_id>/status/', views.update_enquiry_status, name='update_enquiry_status'),
    path('enquiries/<int:enquiry_id>/delete/', views.enquiry_delete, name='enquiry_delete'),

    # Appointments
    path('appointments/', views.appointments, name='appointments'),
    path('appointments/<int:appointment_id>/', views.appointment_detail, name='appointment_detail'),
    path('appointments/<int:appointment_id>/status/', views.update_appointment_status, name='update_appointment_status'),
    path('appointments/<int:appointment_id>/delete/', views.appointment_delete, name='appointment_delete'),

    # Support Requests
    path('support-requests/', views.support_requests, name='support_requests'),
    path('support-requests/<int:request_id>/', views.support_request_detail, name='support_request_detail'),
    path('support-requests/<int:request_id>/status/', views.update_support_request_status, name='update_support_request_status'),
    path('support-requests/<int:request_id>/delete/', views.support_request_delete, name='support_request_delete'),

    # Offers & Announcements Management
    path('offers/', views.offers, name='offers'),
    path('offers/<int:offer_id>/toggle-active/', views.offer_toggle_active, name='offer_toggle_active'),
    path('offers/<int:offer_id>/delete/', views.offer_delete, name='offer_delete'),
    path('announcements/<int:announcement_id>/toggle-active/', views.announcement_toggle_active, name='announcement_toggle_active'),
    path('announcements/<int:announcement_id>/delete/', views.announcement_delete, name='announcement_delete'),

    # Settings
    path('settings/', views.settings_view, name='settings'),

    # Google Sheets Sync Monitoring
    path('google-sheets/', views.google_sheets_sync_monitor, name='google_sheets_sync'),
    path('google-sheets/<int:sync_id>/retry/', views.google_sheets_retry_action, name='google_sheets_retry'),
    path('google-sheets/retry-all-failed/', views.google_sheets_retry_all_failed, name='google_sheets_retry_all_failed'),

    # Live Notifications API
    path('api/notifications/', views.notifications_api, name='notifications_api'),
]

