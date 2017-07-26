"""
Views that control what happens in the system
"""
from wsgiref.util import FileWrapper

from django.apps import AppConfig
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.shortcuts import render, resolve_url, render_to_response, redirect, get_object_or_404
from django.http import *
from django.contrib import auth, messages
from django.template import RequestContext
from django.template.context_processors import csrf
from os import *
from django.contrib.auth.decorators import login_required, user_passes_test
import os
# Load Webpages
from django.utils.encoding import smart_str
from django.views.generic import UpdateView

from PepBandWebsite.forms import changeEBoard, changeSong
from PepBandWebsite.models import Song, eBoard, Section

# Commands that run at startup to initiate the database and song lists.
memeList = []
songList = []

songsList = []
songEntries = []
memeEntries = []

global publicSongList
global totalSongList

publicSongList = []
totalSongList = []

# def foo():
# Generates the list of memes from the pictures in the static folder.  It skips unwanted pictures.
for file in os.listdir('Server/static/media'):
    if (file != ("1Teryn.JPG")) and (file != ("banner.jpg")) and (file != ("favicon.ico")) and (
                    file != ("favicon.png") and file != ("sadtiger.jpg")):
        memeEntries.append(file)

# Adds the name of the files to the list of songs
for folder in os.listdir('Server/static/music'):
    songEntries.append(folder)

# Sorts the list of songs
songEntries = sorted(songEntries)

# If the song isn't in the database, it adds it with the specific slug and title.
for entry in songEntries:
    if Song.objects.filter(title=entry):
        pass
    else:
        if entry is not None:
            slug = entry.replace(" ", "-")
            song = Song(title=entry, slug=slug)
            song.save()

# Generates the song lists
publicSongList = Song.objects.filter(status='Public').order_by('title')
totalSongList = Song.objects.all().order_by('title')
print(totalSongList)


def checkAdmin(user):
    """
    Check to see if the user is in the Admin group
    :param user: Current system user
    :return: Users in the Admin group
    """
    return user.groups.filter(name="Admin")


def checkMember(user):
    """
    Check to see if the user is in the Member group
    :param user: Current system user
    :return: Users in the Member group
    """
    return user.groups.filter(name="Member")


def checkConductor(user):
    """
    Check to see if the user is in the Conductor group
    :param user: Current system user
    :return: Users in the Conductor group
    """
    return user.groups.filter(name="Conductor")


def checkPresident(user):
    """
    Check to see if the user is in the President group
    :param user: Current system user
    :return: Users in the President group
    """
    return user.groups.filter(name="President")


def index(request):
    """
    Landing page for the site
    :param request: Request
    :return: Renders the landing page
    """
    return render(request, "index/index.html")


def notFound(request):
    """
    404 page
    :param request: Request
    :return: Renders the 404 page
    """
    return render(request, "dashboard/404.html")


@user_passes_test(checkAdmin, login_url='/login/')
def admin_page(request):
    users = User.objects.values_list('username', flat=True)
    print(users)
    eBoardList = eBoard.objects.all
    sectionList = Section.objects.all()
    return render(request, "dashboard/admin_page.html",
                  {"eboard": eBoardList, "section": sectionList, "list": totalSongList, "users":users})


@user_passes_test(checkAdmin, login_url='/login/')
def changePassword(request, username):
    realUser = request.user
    request.user = User.objects.get(username=username)
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            request.user = realUser
            return redirect('/')
        else:
            request.user = realUser
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
        request.user = realUser
    return render(request, 'dashboard/change_password.html', {
        'form': form
    })


@user_passes_test(checkAdmin, login_url='/login/')
def deleteSong(request, slug):
    Song.objects.filter(slug=slug).delete()
    global publicSongList
    global totalSongList
    publicSongList = Song.objects.filter(status='Public').order_by('title')
    totalSongList = Song.objects.all().order_by('title')
    return HttpResponseRedirect('/admin_page')


@user_passes_test(checkMember, login_url='/login/')
def eboard(request):
    """
    Loads the page for the eboard information
    :param request: Request
    :return: Renders the eboard page
    """
    eBoardList = eBoard.objects.all
    return render(request, "dashboard/eboard.html", {"list": eBoardList})


@user_passes_test(checkMember, login_url='/login/')
def section_leaders(request):
    """
    Loads the page for the section leader page
    :param request: Request
    :return: Renders the section leader page
    """
    sectionList = Section.objects.all()
    return render(request, "dashboard/section_leaders.html", {"list": sectionList})


@user_passes_test(checkMember, login_url='/login/')
def constitution(request):
    """
    Loads the page for constitution page
    :param request: Request
    :return: Renders the documents page
    """
    return render(request, "dashboard/constitution.html")


@user_passes_test(checkMember, login_url='/login/')
def home(request):
    """
    Loads the page for the dashboard when you login
    :param request: Request
    :return: Renders the dashboard page with the public music and calendar
    """
    # publicSongList = Song.objects.filter(status='Public')
    return render(request, "dashboard/home.html", {"list": publicSongList})


# Login
def login(request):
    """
    Controls the login for the user
    :param request: Request
    :return: Renders the login page
    """
    c = {}
    c.update(csrf(request))
    return render_to_response('dashboard/login.html', c)


def auth_view(request):
    """
    Authenticates the user that is logging in 
    :param request: Request 
    :return: Renders the landing page depending on the user group
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
    :param request: Request
    :return: Render the memes page
    """
    return render(request, 'dashboard/memes.html', {"list": memeEntries})


@user_passes_test(checkMember, login_url='/login/')
def songs(request):
    """
    Heart of the song page that loads all the music
    :param request: Request
    :return: Renders the music page with all the music
    """
    return render(request, 'dashboard/music.html', {"list": totalSongList})


@user_passes_test(checkMember, login_url='/login/')
def show_song(request, slug):
    """
    Page that links the song files, youtube video, and notes if existent
    :param request: Request
    :param slug: Slug for the song (Title with "-" instead of " ")
    :return: Renders the song page
    """
    audio = []
    name = Song.objects.get(slug=slug)
    # address = "Server/static/music"
    address = 'Server/static/music/' + name.title
    for file in os.listdir(address):
        if file.endswith(".wav") or file.endswith(".mp3"):
            audio.append(file)
            print("success")
    return render(request, "dashboard/success.html", {"song": name, "audio": audio})


@user_passes_test(checkConductor, login_url='/login/')
def conductor(request):
    """
    Dashboard for the conductor that allows for the altering of song fields
    :param request: Request
    :return: Renders the conductor dashboard
    """
    return render(request, "dashboard/conductor.html", {"list": totalSongList})


@user_passes_test(checkConductor, login_url='/login/')
def changeStatus(request, slug):
    """
    Toggles the status of the song between Public and Private
    :param request: Request
    :param slug: Slug for the song (Title with "-" instead of " ")
    :return: Redirects to the conductor page
    """
    piece = Song.objects.get(slug=slug)
    if piece.status == "Public":
        piece.status = "Private"
    elif piece.status == "Private":
        piece.status = "Public"
    piece.save()
    global publicSongList
    global totalSongList
    publicSongList = Song.objects.filter(status='Public').order_by('title')
    totalSongList = Song.objects.all().order_by('title')
    return HttpResponseRedirect('/conductor')


@user_passes_test(checkConductor, login_url='/login/')
def changeNotes(request, slug):
    """
    Allows the conductor to change the notes of the selected song
    :param request: Request
    :param slug: Slug for the song (Title with "-" instead of " ")
    :return: Renders the changeInfo page to allow changes to be made
    """
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
    """
    Presidential dashboard that allows the user to see the current eboard and section leaders and allows them to make 
    changes
    :param request: Request 
    :return: Renders the President dashboard
    """
    eBoardList = eBoard.objects.all
    sectionList = Section.objects.all()
    return render(request, "dashboard/president.html", {"eboard": eBoardList, "section": sectionList})


@user_passes_test(checkPresident, login_url='/login/')
def changeEboard(request, id):
    """
    Allows the president to change the fields of the eboard members
    :param request: Request
    :param id: ID of the database entry for the selected position
    :return: Renders the changeInfo page to allow changes to be made
    """
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


@user_passes_test(checkPresident, login_url='/login/')
def changeSection(request, id):
    """
    Allows the president to change the fields of the section leaders
    :param request: Request
    :param id: ID of the database entry for the selected section
    :return: Renders the changeInfo page to allow changes to be made
    """
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


@user_passes_test(checkMember, login_url='/login/')
def jpg(request, slug):
    """
    Loads a list of JPG files for the selected song
    :param request: Request
    :param slug: Slug for the song (Title with "-" instead of " ")
    :return: Renders the jpg file if JPG files exist else 404
    """
    name = Song.objects.get(slug=slug)
    parts = []
    address = 'Server/static/music/' + name.title + '/jpg'
    if os.path.exists(address):
        for folder in listdir(address):
            parts.append(folder)
        return render(request, "dashboard/jpg.html", {"songs": name.title, "parts": parts, "slug": slug})
    else:
        return HttpResponseRedirect('/404')


@user_passes_test(checkMember, login_url='/login/')
def jpgShow(request, slug, part):
    """
    Emebeds a fullpage JPG on a new tab 
    :param request: Request
    :param slug: Slug for the song (Title with "-" instead of " ")
    :param part: What part has been selected
    :return: Renders the page where the JPG file is emebeded
    """
    song = Song.objects.get(slug=slug)
    part = part
    address = "music/" + song.title + "/jpg/" + part
    return render(request, "dashboard/jpgShow.html", {"part": part, "song": song, "address": address})


@user_passes_test(checkMember, login_url='/login/')
def pdf(request, slug):
    """
    Loads a list of PDF files for the selected song
    :param request: Request
    :param slug: Slug for the song (Title with "-" instead of " ")
    :return: Renders the PDF file if files exist else 404
    """
    name = Song.objects.get(slug=slug)
    parts = []
    address = 'Server/static/music/' + name.title + '/pdf'
    if os.path.exists(address):
        for folder in listdir(address):
            parts.append(folder)
        return render(request, "dashboard/pdf.html", {"songs": name.title, "parts": parts, "slug": slug})
    else:
        return HttpResponseRedirect('/404')


@user_passes_test(checkMember, login_url='/login/')
def pdfShow(request, slug, part):
    """
    Emebeds a fullpage PDF on a new tab
    :param request: Request
    :param slug: Slug for the song (Title with "-" instead of " ")
    :param part: What part has been selected
    :return: Renders the page where the PDF file is embeded
    """
    song = Song.objects.get(slug=slug)
    part = part
    address = "music/" + song.title + "/pdf/" + part
    return render(request, "dashboard/pdfShow.html", {"part": part, "song": song, "address": address})
