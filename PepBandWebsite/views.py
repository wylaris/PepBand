"""
View that control what happens in the system
"""
from django.contrib.auth import authenticate, login
from django.shortcuts import render, resolve_url, render_to_response
from django.http import *
from django.contrib import auth
from django.template.context_processors import csrf
from os import listdir, walk

# Load Webpages
from PepBandWebsite.models import Song

memeList = []
songList = []

songsList = []
songEntries = []
memeEntries = []

for file in listdir('Server\static\media'):
    if (file != ("1Teryn.JPG")) and (file != ("banner.jpg")) and (file != ("favicon.ico")) and (
                file != ("favicon.png")):
        memeEntries.append(file)

for folder in listdir('Server\static\music'):
    songEntries.append(folder)

songEntries = sorted(songEntries)

for entry in songEntries:
    if Song.objects.filter(title=entry):
        pass
    else:
        song = Song(title=entry)
        song.save()

publicSongList = Song.objects.filter(status='Pu')
totalSongList = Song.objects.all


def index(request):
    """
    Landing page for the site
    :param request: 
    :return: 
    """
    return render(request, "index/index.html")
    # return HttpResponse("Hello, world.  Welcome to the RIT Pep Band.")


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
    return render(request, "dashboard/home.html", {"list": songEntries})


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

# Login
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


# Dropbox

def memes(request):
    """
    The sweet sweet meme page that has been long awaited
    :param request: 
    :return: 
    """
    return render(request, 'dashboard/memes.html', {"list": memeEntries})


def songs(request):
    """
    Heart of the song page that loads all the music
    :param request: 
    :return: 
    """
    return render(request, 'dashboard/music.html', {"list": totalSongList})


def show_song(request, title):
    return render(request, "dashboard/success.html")
