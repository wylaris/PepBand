from django.shortcuts import render

# Create your views here.
"""
Views that control what happens in the system
"""
import shutil
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
from os import listdir
from django.contrib.auth.decorators import login_required, user_passes_test
import os
from django.core.files import File
import zipfile
# Load Webpages
from django.utils.encoding import smart_str
from django.views.generic import UpdateView
from django.views.static import serve

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
            print("slug = " + entry)
            slug = entry.replace(" ", "-")
            print("This is the updated slug: " + slug)
            slug = slug.replace("'", "-")
            print("This is the updated slug: " + slug)
            slug = slug.replace("(", "-")
            print("This is the updated slug: " + slug)
            slug = slug.replace(")", "-")
            print("This is the updated slug: " + slug)
            slug = slug.replace('!', '-')
            print("This is the final updated slug: " + slug)
            song = Song(title=entry, slug=slug)
            song.save()

# Generates the song lists
publicSongList = Song.objects.filter(status='Public').order_by('title')
totalSongList = Song.objects.all().order_by('title')

# list of mobile User Agents
mobile_uas = [
    'w3c ', 'acs-', 'alav', 'alca', 'amoi', 'audi', 'avan', 'benq', 'bird', 'blac',
    'blaz', 'brew', 'cell', 'cldc', 'cmd-', 'dang', 'doco', 'eric', 'hipt', 'inno',
    'ipaq', 'java', 'jigs', 'kddi', 'keji', 'leno', 'lg-c', 'lg-d', 'lg-g', 'lge-',
    'maui', 'maxo', 'midp', 'mits', 'mmef', 'mobi', 'mot-', 'moto', 'mwbp', 'nec-',
    'newt', 'noki', 'oper', 'palm', 'pana', 'pant', 'phil', 'play', 'port', 'prox',
    'qwap', 'sage', 'sams', 'sany', 'sch-', 'sec-', 'send', 'seri', 'sgh-', 'shar',
    'sie-', 'siem', 'smal', 'smar', 'sony', 'sph-', 'symb', 't-mo', 'teli', 'tim-',
    'tosh', 'tsm-', 'upg1', 'upsi', 'vk-v', 'voda', 'wap-', 'wapa', 'wapi', 'wapp',
    'wapr', 'webc', 'winw', 'winw', 'xda', 'xda-'
]

mobile_ua_hints = ['SymbianOS', 'Opera Mini', 'iPhone']


def mobileBrowser(request):
    ''' Super simple device detection, returns True for mobile devices '''

    mobile_browser = False
    ua = request.META['HTTP_USER_AGENT'].lower()[0:4]

    if (ua in mobile_uas):
        mobile_browser = True
    else:
        for hint in mobile_ua_hints:
            if request.META['HTTP_USER_AGENT'].find(hint) > 0:
                mobile_browser = True

    return mobile_browser


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


def custom404(request):
    if mobileBrowser(request):
        base = "dashboard/m_base.html"
    else:
        base = "dashboard/base.html"
    return render(request, "dashboard/404.html", {"base": base})


def custom500(request):
    if mobileBrowser(request):
        base = "dashboard/m_base.html"
    else:
        base = "dashboard/base.html"
    return render(request, "dashboard/500.html", {"base": base})


def index(request):
    """
    Landing page for the site
    :param request: Request
    :return: Renders the landing page
    """
    if mobileBrowser(request):
        return render(request, "index/m_index.html")
    else:
        return render(request, "index/index.html")


def notFound(request):
    """
    404 page
    :param request: Request
    :return: Renders the 404 page
    """
    if mobileBrowser(request):
        base = "dashboard/m_base.html"
    else:
        base = "dashboard/base.html"
    return render(request, "dashboard/404.html", {"base": base})


@user_passes_test(checkAdmin, login_url='/login/')
def admin_page(request):
    users = User.objects.values_list('username', flat=True)
    eBoardList = eBoard.objects.all
    sectionList = Section.objects.all()
    if mobileBrowser(request):
        base = "dashboard/m_base.html"
    else:
        base = "dashboard/base.html"
    return render(request, "dashboard/admin_page.html",
                  {"eboard": eBoardList, "section": sectionList, "list": totalSongList, "users": users, "base": base})


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
    if mobileBrowser(request):
        base = "dashboard/m_base.html"
    else:
        base = "dashboard/base.html"
    return render(request, 'dashboard/change_password.html', {
        'form': form, "base": base})


@user_passes_test(checkAdmin, login_url='/login/')
def deleteSong(request, slug):
    Song.objects.filter(slug=slug).delete()
    global publicSongList
    global totalSongList
    publicSongList = Song.objects.filter(status='Public').order_by('title')
    totalSongList = Song.objects.all().order_by('title')
    if mobileBrowser(request):
        base = "dashboard/m_base.html"
    else:
        base = "dashboard/base.html"
    return HttpResponseRedirect('/admin_page', {"base": base})


@user_passes_test(checkMember, login_url='/login/')
def eboard(request):
    """
    Loads the page for the eboard information
    :param request: Request
    :return: Renders the eboard page
    """
    eBoardList = eBoard.objects.all
    if mobileBrowser(request):
        base = "dashboard/m_base.html"
    else:
        base = "dashboard/base.html"
    return render(request, "dashboard/eboard.html", {"eboard": eBoardList, "base": base})


@user_passes_test(checkMember, login_url='/login/')
def section_leaders(request):
    """
    Loads the page for the section leader page
    :param request: Request
    :return: Renders the section leader page
    """
    sectionList = Section.objects.all()
    if mobileBrowser(request):
        base = "dashboard/m_base.html"
    else:
        base = "dashboard/base.html"
    return render(request, "dashboard/section_leaders.html", {"section": sectionList, "base": base})


@user_passes_test(checkMember, login_url='/login/')
def constitution(request):
    """
    Loads the page for constitution page
    :param request: Request
    :return: Renders the documents page
    """
    if mobileBrowser(request):
        base = "dashboard/m_base.html"
    else:
        base = "dashboard/base.html"
    return render(request, "dashboard/constitution.html", {"base": base})


@user_passes_test(checkMember, login_url='/login/')
def home(request):
    """
    Loads the page for the dashboard when you login
    :param request: Request
    :return: Renders the dashboard page with the public music and calendar
    """
    if mobileBrowser(request):
        return render(request, "dashboard/m_home.html", {"list": publicSongList})
    else:
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
        if mobileBrowser(request):
            base = "dashboard/m_base.html"
        else:
            base = "dashboard/base.html"
        if user.groups.filter(name="Admin").count():
            return HttpResponseRedirect('/home')
        elif user.groups.filter(name="President").count():
            return HttpResponseRedirect('/president', {"base": base})
        elif user.groups.filter(name="Conductor").count():
            return HttpResponseRedirect('/conductor', {"base": base})
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
    if mobileBrowser(request):
        base = "dashboard/m_base.html"
    else:
        base = "dashboard/base.html"
    return render(request, 'dashboard/memes.html', {"list": memeEntries, "base": base})


@user_passes_test(checkMember, login_url='/login/')
def songs(request):
    """
    Heart of the song page that loads all the music
    :param request: Request
    :return: Renders the music page with all the music
    """
    if mobileBrowser(request):
        base = "dashboard/m_base.html"
    else:
        base = "dashboard/base.html"
    return render(request, 'dashboard/music.html', {"list": totalSongList, "base": base})


@user_passes_test(checkMember, login_url='/login/')
def show_song(request, slug):
    """
    Page that links the song files, youtube video, and notes if existent
    :param request: Request
    :param slug: Slug for the song (Title with "-" instead of " ")
    :return: Renders the song page
    """
    audio = []
    sections = Section.objects.all()
    slug = slug.replace("'", "-")
    name = Song.objects.get(slug=slug)
    address = 'Server/static/music/' + name.title
    parts = []
    partsFinal = []
    addressJPG = 'Server/static/music/' + name.title + '/jpg'
    addressPDF = 'Server/static/music/' + name.title + '/pdf'
    if os.path.exists(addressJPG) and os.path.exists(addressPDF):
        for folder in listdir(addressJPG):
            parts.append(folder)
        for folder in listdir(addressPDF):
            parts.append(folder)
    for part in parts:
        part = part.replace(".jpg", "")
        part = part.replace(".pdf", "")
        partsFinal.append(part)
    partsFinal = list(set(partsFinal))
    partsFinal = sorted(partsFinal)
    if mobileBrowser(request):
        base = "dashboard/m_base.html"
    else:
        base = "dashboard/base.html"
    if os.path.exists(address):
        for file in os.listdir(address):
            if file.endswith(".wav") or file.endswith(".mp3"):
                audio.append(file)
        return render(request, "dashboard/success.html",
                      {"song": name, "audio": audio, "section": sections, "base": base, "parts": partsFinal})
    else:
        return HttpResponseRedirect('/404', {"base": base})


@user_passes_test(checkConductor, login_url='/login/')
def conductor(request):
    """
    Dashboard for the conductor that allows for the altering of song fields
    :param request: Request
    :return: Renders the conductor dashboard
    """
    if mobileBrowser(request):
        base = "dashboard/m_base.html"
    else:
        base = "dashboard/base.html"
    return render(request, "dashboard/conductor.html", {"list": totalSongList, "base": base})


@user_passes_test(checkConductor, login_url='/')
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
    if mobileBrowser(request):
        base = "dashboard/m_base.html"
    else:
        base = "dashboard/base.html"
    if request.user.is_superuser:
        return HttpResponseRedirect('/admin_page', {"base": base})
    elif checkPresident(request.user):
        return HttpResponseRedirect('/president', {"base": base})
    else:
        return HttpResponseRedirect('/conductor', {"base": base})

@user_passes_test(checkConductor, login_url='/')
def allChange(request):
    for song in Song:
        song.status = 'Public'
        song.save()
    global publicSongList
    global totalSongList
    publicSongList = Song.objects.filter(status='Public').order_by('title')
    totalSongList = Song.objects.all().order_by('title')
    if mobileBrowser(request):
        base = "dashboard/m_base.html"
    else:
        base = "dashboard/base.html"
    if request.user.is_superuser:
        return HttpResponseRedirect('/admin_page', {"base": base})
    elif checkPresident(request.user):
        return HttpResponseRedirect('/president', {"base": base})
    else:
        return HttpResponseRedirect('/conductor', {"base": base})


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
    if mobileBrowser(request):
        base = "dashboard/m_base.html"
    else:
        base = "dashboard/base.html"
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        if request.user.is_superuser:
            return HttpResponseRedirect('/admin_page', {"base": base})
        elif checkPresident(request.user):
            return HttpResponseRedirect('/president', {"base": base})
        else:
            return HttpResponseRedirect('/conductor', {"base": base})
    context = {
        "notes": instance.notes,
        "instance": instance,
        "form": form
    }
    return render(request, "dashboard/changeInfo.html", context, {"base": base})


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
    if mobileBrowser(request):
        base = "dashboard/m_base.html"
    else:
        base = "dashboard/base.html"
    return render(request, "dashboard/president.html",
                  {"eboard": eBoardList, "section": sectionList, "list": totalSongList, "base": base})


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
        if request.user.is_superuser:
            return redirect('/admin_page')
        else:
            return redirect("/president")
    context = {
        "firstName": instance.firstName,
        "lastName": instance.lastName,
        "cell": instance.cell,
        "email": instance.email,
        "instance": instance,
        "form": form
    }
    if mobileBrowser(request):
        base = "dashboard/m_base.html"
    else:
        base = "dashboard/base.html"
    return render(request, "dashboard/changeInfo.html", context, {"base": base})


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
        if request.user.is_superuser:
            return redirect('/admin_page')
        else:
            return redirect("/president")
    context = {
        "firstName": instance.firstName,
        "lastName": instance.lastName,
        "cell": instance.cell,
        "email": instance.email,
        "instance": instance,
        "form": form
    }
    if mobileBrowser(request):
        base = "dashboard/m_base.html"
    else:
        base = "dashboard/base.html"
    return render(request, "dashboard/changeInfo.html", context, {"base": base})


@user_passes_test(checkMember, login_url='/login/')
def jpg(request, slug, section):
    """
    Loads a list of JPG files for the selected song
    :param request: Request
    :param slug: Slug for the song (Title with "-" instead of " ")
    :return: Renders the jpg file if JPG files exist else 404
    """
    name = Song.objects.get(slug=slug)
    parts = []
    address = 'Server/static/music/' + name.title + '/jpg'
    if section != "Percussion":
        if section == "Saxophones":
            section = section.replace("Saxophones", "AltoSax")
        elif section == "Tenor-Saxophones":
            section = section.replace("Tenor-Saxophones", "TenorSax")
        section = section.replace("s", "")
    if mobileBrowser(request):
        base = "dashboard/m_base.html"
    else:
        base = "dashboard/base.html"
    if os.path.exists(address):
        for folder in listdir(address):
            if section in folder:
                parts.append(folder)
        return render(request, "dashboard/jpg.html", {"songs": name.title, "parts": parts, "slug": slug, "base": base})
    else:
        return HttpResponseRedirect('/404', {"base": base})


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
    if mobileBrowser(request):
        base = "dashboard/m_base.html"
    else:
        base = "dashboard/base.html"
    return render(request, "dashboard/jpgShow.html", {"part": part, "song": song, "address": address})


@user_passes_test(checkMember, login_url='/login/')
def pdf(request, slug, section):
    """
    Loads a list of PDF files for the selected song
    :param request: Request
    :param slug: Slug for the song (Title with "-" instead of " ")
    :return: Renders the PDF file if files exist else 404
    """
    name = Song.objects.get(slug=slug)
    parts = []
    address = 'Server/static/music/' + name.title + '/pdf'
    if section != "Percussion":
        if section == "Saxophones":
            section = section.replace("Saxophones", "AltoSax")
        elif section == "Tenor-Saxophones":
            section = section.replace("Tenor-Saxophones", "TenorSax")
        section = section.replace("s", "")
    if mobileBrowser(request):
        base = "dashboard/m_base.html"
    else:
        base = "dashboard/base.html"
    if os.path.exists(address):
        for folder in listdir(address):
            if section in folder:
                parts.append(folder)
        return render(request, "dashboard/pdf.html", {"songs": name.title, "parts": parts, "slug": slug, "base": base})
    else:
        return HttpResponseRedirect('/404', {"base": base})


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
    address = "Server/static/music/" + song.title + "/pdf/" + part
    with open(address, 'rb') as pdf:
        response = HttpResponse(pdf.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'filename=some_file.pdf'
        return response
        # return render(request, "dashboard/pdfShow.html", {"part": part, "song": song, "address": address})


def pickSection(request):
    """
    Renders a page that allows the user to download all the parts for a section
    :param request: Request
    :return: Renders the page where all sections appear as a button
    """
    sections = Section.objects.all()
    role = []
    for section in sections:
        replaced = section.section
        replaced = replaced.replace(" ", "-")
        role.append(replaced)
    if mobileBrowser(request):
        base = "dashboard/m_base.html"
    else:
        base = "dashboard/base.html"
    return render(request, "dashboard/pick_section.html", {"sections": role, "base": base})


def downloadParts(request, section):
    """
    Allows the user to download a zipfile with all the songs for the selected section
    :param request: Request
    :param section: Section selected
    :return: Downloads a zipfile of the parts
    """
    staticSection = section
    address = "Server/static/zipFiles/" + section
    pathOrigin = "Server/static/music/"
    if os.path.exists(address):
        shutil.rmtree(address)
    os.mkdir(address)
    if section != "Percussion":
        if section == "Saxophones":
            section = section.replace("Saxophones", "AltoSax")
        elif section == "Tenor-Saxophones":
            section = section.replace("Tenor-Saxophones", "TenorSax")
        section = section.replace("s", "")
        for entry in totalSongList:
            subFolder = address + "/" + entry.title
            if not os.path.exists(subFolder):
                os.mkdir(subFolder)
                pathSecond = pathOrigin + entry.title + "/jpg/"
                if os.path.exists(pathSecond):
                    for file in os.listdir(pathSecond):
                        if section in file:
                            pathFinal = pathSecond + file
                            shutil.copyfile(pathFinal, address + "/" + entry.title + "/" + file)
    zf = zipfile.ZipFile("Server/static/zipFiles/" + staticSection + ".zip", "w")
    for dirname, subdirs, files in os.walk("Server/static/zipFiles/" + staticSection):
        zf.write(dirname)
        for filename in files:
            zf.write(os.path.join(dirname, filename))
    zf.close()
    filepath = "Server/static/zipFiles/" + staticSection + ".zip"
    return serve(request, os.path.basename(filepath), os.path.dirname(filepath))

