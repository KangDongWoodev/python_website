# apps/attendance/views.py

from django.shortcuts import render

def index(request):
    return render(request, 'attendance/home.html')