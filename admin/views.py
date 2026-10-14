from django.shortcuts import render
from django.http import HttpResponse

def dashboard(request):
    return HttpResponse("<h1>Custom Admin App Dashboard</h1><p>Admin app is configured and ready.</p>")
