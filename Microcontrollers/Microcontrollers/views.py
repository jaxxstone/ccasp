from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http.response import HttpResponseRedirect
from django.contrib.auth.models import AnonymousUser

def index(request):
    return render(request, "index.html")

def login(request):
    return render(request, "overview.html")

def logout(request):
    logout(request)
    request.session.flush()
    request.user = AnonymousUser

    return HttpResponseRedirect('accounts/loggedout/')
