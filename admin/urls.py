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

    # Categories Management
    path('categories/', views.categories, name='categories'),
    path('categories/add/', views.category_create, name='category_create'),
    path('categories/<int:category_id>/edit/', views.category_edit, name='category_edit'),
    path('categories/<int:category_id>/toggle-active/', views.category_toggle_active, name='category_toggle_active'),

    # Enquiries
    path('enquiries/', views.enquiries, name='enquiries'),
    path('enquiries/<int:enquiry_id>/', views.enquiry_detail, name='enquiry_detail'),
    path('enquiries/<int:enquiry_id>/status/', views.update_enquiry_status, name='update_enquiry_status'),

    # Appointments
    path('appointments/', views.appointments, name='appointments'),
    path('appointments/<int:appointment_id>/', views.appointment_detail, name='appointment_detail'),
    path('appointments/<int:appointment_id>/status/', views.update_appointment_status, name='update_appointment_status'),

    # Support Requests
    path('support-requests/', views.support_requests, name='support_requests'),
    path('support-requests/<int:request_id>/', views.support_request_detail, name='support_request_detail'),
    path('support-requests/<int:request_id>/status/', views.update_support_request_status, name='update_support_request_status'),

    # Offers & Settings
    path('offers/', views.offers, name='offers'),
    path('settings/', views.settings_view, name='settings'),
]
