from django.shortcuts import render

def dashboard(request):
    return render(request, 'custom_admin/index.html')

def services(request):
    return render(request, 'custom_admin/services.html')

def enquiries(request):
    return render(request, 'custom_admin/enquiries.html')

def appointments(request):
    return render(request, 'custom_admin/appointments.html')

def offers(request):
    return render(request, 'custom_admin/offers.html')

def settings_view(request):
    return render(request, 'custom_admin/settings.html')

