"""
View that control what happens in the system
"""
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render, resolve_url, render_to_response
from django.http import *
from django.contrib import auth
from django.template.context_processors import csrf
from os import listdir, walk
from django.contrib.auth.decorators import login_required, user_passes_test

# Load Webpages
from PepBandWebsite.models import Song, eBoard, Section

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

eBoardList = eBoard.objects.all
sectionList = Section.objects.all()


def checkAdmin(user):
    return user.groups.filter(name="Admin")


def checkMember(user):
    return user.groups.filter(name="Member")


def checkConductor(user):
    return user.groups.filter(name="Conductor")


def checkPresident(user):
    return user.groups.filter(name="President")


def index(request):
    """
    Landing page for the site
    :param request: 
    :return: 
    """
    return render(request, "index/index.html")


@user_passes_test(checkMember, login_url='/login/')
def eboard(request):
    """
    Loads the page for the eboard information
    :param request: 
    :return: 
    """

    return render(request, "dashboard/eboard.html", {"list": eBoardList})


@user_passes_test(checkMember, login_url='/login/')
def section_leaders(request):
    """
    Loads the page for the section leader page
    :param request: 
    :return: 
    """
    return render(request, "dashboard/section_leaders.html", {"list": sectionList})


@user_passes_test(checkMember, login_url='/login/')
def constitution(request):
    """
    Loads the page for constitution page
    :param request: 
    :return: 
    """
    return render(request, "dashboard/constitution.html")


@user_passes_test(checkMember, login_url='/login/')
def home(request):
    """
    Loads the page for the dashboard when you login
    :param request: 
    :return: 
    """
    return render(request, "dashboard/home.html", {"list": publicSongList})


@user_passes_test(checkAdmin, login_url='/login/')
def admin_page(request):
    """
    Loads the admin page to give tools to admin
    :param request: 
    :return: 
    """
    return render(request, "dashboard/admin_page.html")


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


def auth_view(request):
    """
    Authenticates the user that is logging in 
    :param requst: 
    :return: 
    """
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)

    if user is not None:
        auth.login(request, user)
        if user.groups.filter(name="Conductor").count():
            return HttpResponseRedirect('/conductor')
        elif user.groups.filter(name="President").count():
            return HttpResponseRedirect('/president')
        else:
            return HttpResponseRedirect('/home')
    else:
        return HttpResponseRedirect('/')


@user_passes_test(checkMember, login_url='/login/')
def memes(request):
    """
    The sweet sweet meme page that has been long awaited
    :param request: 
    :return: 
    """
    return render(request, 'dashboard/memes.html', {"list": memeEntries})


@user_passes_test(checkMember, login_url='/login/')
def songs(request):
    """
    Heart of the song page that loads all the music
    :param request: 
    :return: 
    """
    return render(request, 'dashboard/music.html', {"list": totalSongList})


def show_song(request, title):
    return render(request, "dashboard/success.html")


@user_passes_test(checkConductor, login_url='/login/')
def conductor(request):
    return render(request, "dashboard/conductor.html", {"list": totalSongList})


@user_passes_test(checkPresident, login_url='/login/')
def president(request):
    return render(request, "dashboard/president.html")
