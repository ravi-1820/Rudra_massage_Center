from django.urls import path
from . import views

app_name = 'custom_admin'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('services/', views.services, name='services'),
    path('enquiries/', views.enquiries, name='enquiries'),
    path('appointments/', views.appointments, name='appointments'),
    path('offers/', views.offers, name='offers'),
    path('settings/', views.settings_view, name='settings'),
]
