"""
View that control what happens in the system
"""
from django.contrib.auth import authenticate, login
from django.shortcuts import render, resolve_url, render_to_response
from django.http import *
from django.contrib import auth
from django.template.context_processors import csrf
from django.template import RequestContext
import dropbox


#Load Webpages
from PepBandWebsite.models import Song


def index(request):
    """
    Landing page for the site
    :param request: 
    :return: 
    """
    return render(request, "index/index.html")
    #return HttpResponse("Hello, world.  Welcome to the RIT Pep Band.")

def eboard(request):
    """
    Loads the page for the eboard information
    :param request: 
    :return: 
    """
    return render(request, "dashboard/eboard.html")

def section_leaders(request):
    """
    Loads the page for the section leader page
    :param request: 
    :return: 
    """
    return render(request, "dashboard/section_leaders.html")

def constitution(request):
    """
    Loads the page for constitution page
    :param request: 
    :return: 
    """
    return render(request, "dashboard/constitution.html")

def home(request):
    """
    Loads the page for the dashboard when you login
    :param request: 
    :return: 
    """
    return render(request, "dashboard/home.html")

def admin_page(request):
    """
    Loads the admin page to give tools to admin
    :param request: 
    :return: 
    """
    return render(request, "dashboard/admin_page.html")

# def new_song(request):
#     form = Song()
#     if request.method == 'POST':
#         form = Song(request.POST)
#         if form.is_valid():
#             print("Form is valid")
#             form.save()
#             args['success'] = True
#         else:
#             print("Form is not valid")
#     return render(request, 'dashboard/admin_page.html')

#Login
def login(request):
    """
    Controls the login for the user
    :param request: 
    :return: 
    """
    c = {}
    c.update(csrf(request))
    return render_to_response('dashboard/login.html', c)

def auth_view(requst):
    """
    Authenticates the user that is logging in 
    :param requst: 
    :return: 
    """
    username = requst.POST.get('username', '')
    password = requst.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)

    if user is not None:
        auth.login(requst, user)
        return HttpResponseRedirect('/home')
    else:
        return HttpResponseRedirect('/')

#Dropbox

def memes(request):
    """
    The sweet sweet meme page that has been long awaited
    :param request: 
    :return: 
    """
    memeList = dropbox.Dropbox('3Ib-6gw6SkAAAAAAAAAAifOLl9FjWeqovxj166ITwfh-lB7mJMQCB0kjM_he0Ajd')
    for entry in memeList.files_list_folder('').entries:
        print("   ", entry.name)
        File = type(entry)

    entries = []
    for entry in memeList.files_list_folder('/Testing').entries:
        print("   ", entry, type(entry))
        entries.append(entry)
        if type(entry) == File:
            print("       ", "This is a File")
        else:
            print("       ", "This is a Folder")
    return render(request, 'dashboard/memes.html', {"list": entries})

def songs(request):
    """
    Heart of the song page that loads all the music
    :param request: 
    :return: 
    """
    pass