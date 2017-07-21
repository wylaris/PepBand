"""
View that control what happens in the system
"""
from django.apps import AppConfig
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render, resolve_url, render_to_response, redirect, get_object_or_404
from django.http import *
from django.contrib import auth
from django.template import RequestContext
from django.template.context_processors import csrf
from os import *
from django.contrib.auth.decorators import login_required, user_passes_test
import os
# Load Webpages
from django.views.generic import UpdateView

from PepBandWebsite.forms import changeEBoard, changeSong
from PepBandWebsite.models import Song, eBoard, Section

memeList = []
songList = []

songsList = []
songEntries = []
memeEntries = []

global publicSongList
global totalSongList

publicSongList = []
totalSongList = []

# class MyAppConfig(AppConfig, songEntries, memeEntries):
#     def ready(self, songEntries, memeEntries):
# def foo():
for file in listdir('Server\static\media'):
    if (file != ("1Teryn.JPG")) and (file != ("banner.jpg")) and (file != ("favicon.ico")) and (
                    file != ("favicon.png") and file != ("sadtiger.jpg")):
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

publicSongList = Song.objects.filter(status='Public')
totalSongList = Song.objects.all


# return publicSongList, totalSongList

# def loadSongLists(public, total):
#     publicSongList = public
#     totalSongList = total
#     return publicSongList, totalSongList


# eBoardList = eBoard.objects.all
# sectionList = Section.objects.all()


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


def notFound(request):
    return render(request, "dashboard/404.html")


@user_passes_test(checkMember, login_url='/login/')
def eboard(request):
    """
    Loads the page for the eboard information
    :param request: 
    :return: 
    """
    eBoardList = eBoard.objects.all
    return render(request, "dashboard/eboard.html", {"list": eBoardList})


@user_passes_test(checkMember, login_url='/login/')
def section_leaders(request):
    """
    Loads the page for the section leader page
    :param request: 
    :return: 
    """
    sectionList = Section.objects.all()
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
    # publicSongList = Song.objects.filter(status='Public')
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
        if user.groups.filter(name="Admin").count():
            return HttpResponseRedirect('/home')
        elif user.groups.filter(name="Conductor").count():
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
    totalSongList = Song.objects.all
    return render(request, 'dashboard/music.html', {"list": totalSongList})


def show_song(request, slug):
    name = Song.objects.get(slug=slug)
    return render(request, "dashboard/success.html", {"song": name})


@user_passes_test(checkConductor, login_url='/login/')
def conductor(request):
    # totalSongList = Song.objects.all
    return render(request, "dashboard/conductor.html", {"list": totalSongList})


def changeStatus(request, slug):
    piece = Song.objects.get(slug=slug)
    if piece.status == "Public":
        piece.status = "Private"
    elif piece.status == "Private":
        piece.status = "Public"
    piece.save()
    global publicSongList
    global totalSongList
    publicSongList = Song.objects.filter(status='Public')
    totalSongList = Song.objects.all
    return HttpResponseRedirect('/conductor')

def changeNotes(request, slug):
    instance = get_object_or_404(Song, slug=slug)
    form = changeSong(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return redirect("/conductor")
    context = {
        "notes": instance.notes,
        "instance": instance,
        "form": form
    }
    return render(request, "dashboard/changeInfo.html", context)


@user_passes_test(checkPresident, login_url='/login/')
def president(request):
    eBoardList = eBoard.objects.all
    sectionList = Section.objects.all()
    return render(request, "dashboard/president.html", {"eboard": eBoardList, "section": sectionList})


def changeEboard(request, id):
    instance = get_object_or_404(eBoard, id=id)
    form = changeEBoard(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return redirect("/president")
    context = {
        "firstName": instance.firstName,
        "lastName": instance.lastName,
        "cell": instance.cell,
        "email": instance.email,
        "instance": instance,
        "form": form
    }
    return render(request, "dashboard/changeInfo.html", context)


def changeSection(request, id):
    instance = get_object_or_404(Section, id=id)
    form = changeEBoard(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return redirect("/president")
    context = {
        "firstName": instance.firstName,
        "lastName": instance.lastName,
        "cell": instance.cell,
        "email": instance.email,
        "instance": instance,
        "form": form
    }
    return render(request, "dashboard/changeInfo.html", context)


def jpg(request, slug):
    name = Song.objects.get(slug=slug)
    parts = []
    address = 'Server/static/music/' + name.title + '/jpg'
    if os.path.exists(address):
        for folder in listdir(address):
            parts.append(folder)
        return render(request, "dashboard/jpg.html", {"songs": name.title, "parts": parts, "slug": slug})
    else:
        return HttpResponseRedirect('/404')


def jpgShow(request, slug, part):
    song = Song.objects.get(slug=slug)
    part = part
    address = "music/" + song.title + "/jpg/" + part
    return render(request, "dashboard/jpgShow.html", {"part": part, "song": song, "address": address})


def pdf(request, slug):
    name = Song.objects.get(slug=slug)
    parts = []
    address = 'Server/static/music/' + name.title + '/pdf'
    if os.path.exists(address):
        for folder in listdir(address):
            parts.append(folder)
        return render(request, "dashboard/pdf.html", {"songs": name.title, "parts": parts, "slug": slug})
    else:
        return HttpResponseRedirect('/404')


def pdfShow(request, slug, part):
    song = Song.objects.get(slug=slug)
    part = part
    address = "music/" + song.title + "/pdf/" + part
    return render(request, "dashboard/pdfShow.html", {"part": part, "song": song, "address": address})
