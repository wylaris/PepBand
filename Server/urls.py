"""untitled URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from PepBandWebsite import views
from Server import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls), #URL for the admin site
    url(r'^$', views.index, name='index'), #URL for the landing page
    #url(r'^login/$', views.login, name='login'), #URL for the login page (not being used)
    url(r'^auth/$', views.auth_view, name='auth_view'), #URL for the authentication page
    url(r'^404/$', views.notFound, name='notFound'),  # URL for the 404 page
    url(r'^eboard/$', views.eboard, name='eboard'),  #URL for the eboard page
    url(r'^section_leaders/$', views.section_leaders, name='section_leaders'), #URL for the section leader page
    url(r'^documents/$', views.constitution, name='documents'),  #URL for the documents page
    url(r'^home/$', views.home, name='home'),  #URL for the dashboard page
    url(r'^admin_page/$', views.admin_page, name='admin_page'),  #URL for the admin page (no being used)
    url(r'^admin_page/(?P<slug>.*)/delete/$', views.deleteSong, name='deleteSong'),
    url(r'^admin_page/(?P<username>.*)/change_password/$', views.changePassword, name='changePassword'),
    url(r'^memes/$', views.memes, name='memes'),  #URL for the memes page
    url(r'^music/$', views.songs, name='songs'),  # URL for the music page
    url(r'^music/(?P<slug>[\w\-]+)/$', views.show_song, name='songHandler'), #URL for the single song page
    url(r'^music/(?P<slug>[\w\-]+)/jpg/(?P<section>.*)/$', views.jpg, name='songHandler'),  # URL for the JPG parts for a single song
    url(r'^music/(?P<slug>[\w\-]+)/show/(?P<part>.*)/$', views.jpgShow, name='songHandler'),  # URL for the page that emebeds the JPG file
    url(r'^music/(?P<slug>[\w\-]+)/pdf/(?P<section>.*)/$', views.pdf, name='songHandler'),  # URL for the PDF
    url(r'^music/(?P<slug>[\w\-]+)/(?P<part>.*)/$', views.pdfShow, name='songHandler'),  # URL for the page that emebeds the JPG file
    url(r'^conductor/$', views.conductor, name='conductor'),  # URL for the conductor page
    url(r'^conductor/(?P<slug>[\w\-]+)/$', views.changeStatus, name='changeStatus'),  # URL for the page that changes the status of a song
    url(r'^conductor/(?P<slug>[\w\-]+)/change/$', views.changeNotes, name='changeStatus'),  # URL for the page that changes that notes of a song
    url(r'^president/$', views.president, name='president'),  # URL for the president page
    url(r'^president/eboard/(?P<id>[\w\-]+)/$', views.changeEboard, name='songs'),  # URL for the page that changes fields for a eboard entry
    url(r'^president/section/(?P<id>[\w\-]+)/$', views.changeSection, name='songs'),  # URL for the page that changes fields for a section leader entry
    url(r'^pick_section/$', views.pickSection, name='pick_section'),  # URL for the pick section page
    url(r'^pick_section/(?P<section>.*)/download/$', views.downloadParts, name='downlaodParts'),  # URL for the download music page
]
