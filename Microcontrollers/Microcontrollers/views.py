'''This module contains the logic for rendering pages for the Microcontrollers
application. It handles the index view, login view, and logout views.'''

from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http.response import HttpResponseRedirect
from django.contrib.auth.models import AnonymousUser

def index(request):
    '''
    View for index.html, /, landing page
    @param request: the HTTP GET request
    @return: rendered index.html page
    '''
    return render(request, "index.html")

def login(request):
    '''
    View returned after successful login attempt
    @param request: the HTTP GET request
    @return: rendered overview.html page
    '''
    return render(request, "overview.html")

def logout(request):
    '''
    View for logout request. Flushes session and logs out user
    @param request: the HTTP GET request
    @return: rendered index.html page
    '''
    logout(request)
    request.session.flush()
    request.user = AnonymousUser
    return HttpResponseRedirect('accounts/loggedout/')
