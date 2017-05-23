
from django.contrib.auth import authenticate, login
from django.shortcuts import render, resolve_url, render_to_response
from django.http import *
from django.contrib import auth
from django.template.context_processors import csrf
from django.template import RequestContext


#Load Webpages
from PepBandWebsite.models import Song


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

def admin_page(request):
    return render(request, "dashboard/admin_page.html")

def new_song(request):
    form = Song()
    if request.method == 'POST':
        form = Song(request.POST)
        if form.is_valid():
            print("Form is valid")
            form.save()
            args['success'] = True
        else:
            print("Form is not valid")
    return render(request, 'dashboard/admin_page.html')

#Login
def login(request):
    c = {}
    c.update(csrf(request))
    return render_to_response('dashboard/login.html', c)

def auth_view(requst):
    username = requst.POST.get('username', '')
    password = requst.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)

    if user is not None:
        auth.login(requst, user)
        return HttpResponseRedirect('/home')
    else:
        return HttpResponseRedirect('/')