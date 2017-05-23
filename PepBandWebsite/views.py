
from django.contrib.auth import authenticate, login
from django.shortcuts import render, resolve_url, render_to_response
from django.http import *
from django.contrib import auth
from django.template.context_processors import csrf


#Load Webpages
def index(request):
    return render(request, "index/index.html")
    #return HttpResponse("Hello, world.  Welcome to the RIT Pep Band.")

def eboard(request):
    return render(request, "dashboard/eboard.html")

def section_leaders(request):
    return render(request, "dashboard/section_leaders.html")

def constitution(request):
    return render(request, "dashboard/constitution.html")

def home(request):
    return render(request, "dashboard/home.html")

#Login
def login(request):
    c = {}
    c.update(csrf(request))
    return render_to_response('dashboard/login.html', c)