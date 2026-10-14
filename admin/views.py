from django.shortcuts import render

def dashboard(request):
    return render(request, 'admin/index.html')

def services(request):
    return render(request, 'admin/services.html')

def enquiries(request):
    return render(request, 'admin/enquiries.html')

def appointments(request):
    return render(request, 'admin/appointments.html')

def offers(request):
    return render(request, 'admin/offers.html')

def settings_view(request):
    return render(request, 'admin/settings.html')
