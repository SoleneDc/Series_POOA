from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template import loader
from django.contrib.auth.models import User
from django.contrib.auth import *
from django.core import serializers
from .forms import *
import json
import services
"""This class defines the controllers for the application
each fonction is supposed to process a page and send it to the url mapper"""

def index(request):
    service = services.Services()
    template = loader.get_template('index.html')
    bestseries = service.discover_best_series()
    airingseries = service.discover_series_on_the_air()
    context = {'bestseries' : bestseries, 'airingseries': airingseries}
    return HttpResponse(template.render(request=request, context = context))

def register(request):
    template = loader.get_template('register.html')
    return HttpResponse(template.render(request=request))

def search(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = SearchForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            if request.POST.get('tick')=="series":
                service = services.Services()  # charge service
                template = loader.get_template('searchResult.html')  # charge la page html
                # request.POST['search'] est la chaine de caractères entrée en recherche par l'user
                response = service.search_series_names(
                    request.POST['search'])  # effectue la recherche et r&cupere la réponse
                context = {'response': response}
                return HttpResponse(template.render(request=request, context=context))

            elif request.POST.get('tick')=="people":
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
                service = services.Services()  # charge service
                template = loader.get_template('searchPeople.html')  # charge la page html
                # request.POST['search'] est la chaine de caractères entrée en recherche par l'user
                response = service.search_people(request.POST['search'])  # effectue la recherche et r&cupere la réponse
                context = {'response': response}
                return HttpResponse(template.render(request=request, context=context))

            else:
                raise EnvironmentError
    # if a GET (or any other method) we'll create a blank form//
    else:
        form = SearchForm()

    return render(request, 'index.html', {'form': form})


def signIn(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = RegisterForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:*
            user = User.objects.create_user(form.data['first_name'], form.data['email'], form.data['password'])
            user.last_name = form.data['last_name']
            user.save()
            context={'name' : user.first_name}
            return HttpResponseRedirect('/welcome/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = RegisterForm()

    return render(request, 'index.html', {'form': form})


def welcome(request):
    template = loader.get_template('welcome.html')
    return HttpResponse(template.render(request=request))

def logIn(request):
    user = authenticate(username=request.POST['user_name'], password=request.POST['password'])
    if user is not None:
        user ={'first_name': user.first_name, 'id' : user.id, 'last_name' : user.last_name}
        request.session['user'] = user
        json_response = {'status': 'OK', 'user': user}
        return HttpResponse(json.dumps(json_response),
                            content_type='application/json')
    else:
        json_response = {'status': 'KO'}
        return HttpResponse(json.dumps(json_response),
                            content_type='application/json')
def logOut(request):
    logout(request)
    return index(request)

def genre(request):
    #rajouter ici une fonction qui renvoie la liste des genres
    return True