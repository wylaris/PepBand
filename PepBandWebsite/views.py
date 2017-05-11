from django.shortcuts import render
from django.http import *

def index(request):
    return render(request, "index/index.html")
    #return HttpResponse("Hello, world.  Welcome to the RIT Pep Band.")