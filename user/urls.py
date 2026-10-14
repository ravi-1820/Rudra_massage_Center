from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('service-detail/', views.service_detail, name='service_detail'),
    path('appointment/', views.appointment, name='appointment'),
    path('blog/', views.blog, name='blog'),
    path('blog-detail/', views.blog_detail, name='blog_detail'),
    path('bmi-calculator/', views.bmi_calculator, name='bmi_calculator'),
    path('certificates/', views.certificates, name='certificates'),
    path('contact/', views.contact, name='contact'),
    path('digital-profile/', views.digital_profile, name='digital_profile'),
    path('enquiry/', views.enquiry, name='enquiry'),
    path('faq/', views.faq, name='faq'),
    path('gallery/', views.gallery, name='gallery'),
    path('offers/', views.offers, name='offers'),
    path('support/', views.support, name='support'),
    path('testimonials/', views.testimonials, name='testimonials'),
]
