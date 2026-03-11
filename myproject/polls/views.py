from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def testView(request):
    return HttpResponse("test view")

def landingPage(request):
    return HttpResponse("Hello, world. You're on the landing page.")
