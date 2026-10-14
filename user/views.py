from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return HttpResponse("<h1>Welcome to Rudra Massage Center</h1><p>Django project is set up successfully!</p><p><a href='/admin/'>Go to Django Admin</a></p>")
