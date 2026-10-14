from django.shortcuts import render

def home(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def services(request):
    return render(request, 'services.html')

def service_detail(request):
    return render(request, 'service-detail.html')

def appointment(request):
    return render(request, 'appointment.html')

def blog(request):
    return render(request, 'blog.html')

def blog_detail(request):
    return render(request, 'blog-detail.html')

def bmi_calculator(request):
    return render(request, 'bmi-calculator.html')

def certificates(request):
    return render(request, 'certificates.html')

def contact(request):
    return render(request, 'contact.html')

def digital_profile(request):
    return render(request, 'digital-profile.html')

def enquiry(request):
    return render(request, 'enquiry.html')

def faq(request):
    return render(request, 'faq.html')

def gallery(request):
    return render(request, 'gallery.html')

def offers(request):
    return render(request, 'offers.html')

def support(request):
    return render(request, 'support.html')

def testimonials(request):
    return render(request, 'testimonials.html')
