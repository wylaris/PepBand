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

urlpatterns = [
    url(r'^admin/', admin.site.urls), #URL for the admin site
    url(r'^$', views.index, name='index'), #URL for the landing page
    url(r'^login/$', views.login, name='login'), #URL for the login page (will be the landing page)
    url(r'^auth/$', views.auth_view, name='auth_view'), #URL for the authentication page
    url(r'^eboard/$', views.eboard, name='eboard'),  #URL for the eboard page
    url(r'^section_leaders/$', views.section_leaders, name='section_leaders'), #URL for the section leader page
    url(r'^constitution/$', views.constitution, name='constitution'),  #URL for the constitution page
    url(r'^home/$', views.home, name='home'),  #URL for the dashboard page
    url(r'^admin_page/$', views.admin_page, name='admin_page'),  #URL for the admin page
    #url(r'^new_song/$', views.new_song, name='new_song'),  #URL for adding a song to the database
    url(r'^memes/$', views.memes, name='memes'),  #URL for the memes page
    #url(r'^music/$', views.songs, name='songs'), #URL for the music page
    #url(r'^music/music/$', views.music, name='music'), #URL for the private music server
]
