from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template import loader
from django.contrib.auth.models import User
from .forms import *
import services
"""This class defines the controllers for the application
each fonction is supposed to process a page and send it to the url mapper"""

def index(request):
    service = services.Services()
    template = loader.get_template('index.html')
    bestseries = service.discover_best_series()
    context = {'bestseries' : bestseries}
    return HttpResponse(template.render(request=request, context = context))

# def index(request):
#     service = services.Services()
#     template = loader.get_template('index.html')
#     bestseries = service.discover_best_series()
#     context = {'bestseries' : bestseries}
#     rank = 1
#     for series in bestseries:
#         context['betsteries'][rank] = series
#         rank += 1
#     return HttpResponse(template.render(request=request, context = context))



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
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            service = services.Services()  # charge service
            template = loader.get_template('searchResult.html')  # charge la page html
            # request.POST['search'] est la chaine de caractères entrée en recherche par l'user
            response = service.search_series_names(request.POST['search'])  # effectue la recherche et r&cupere la réponse
            context = {'response': response}
            return HttpResponse(template.render(request=request, context=context))
    # if a GET (or any other method) we'll create a blank form
    else:
        form = SearchForm(request.POST)
        print (form.errors)

    return render(request, 'index.html', {'form': form})

def search_people(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = SearchForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            service = services.Services()  # charge service
            template = loader.get_template('searchPeople.html')  # charge la page html
            # request.POST['search'] est la chaine de caractères entrée en recherche par l'user
            response = service.search_people(request.POST['searchp'])  # effectue la recherche et r&cupere la réponse
            context = {'response': response}
            AFFICHAGE = HttpResponse(template.render(request=request, context=context))
            for item in AFFICHAGE:


    # if a GET (or any other method) we'll create a blank form
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

def discoverBestSeries(request):
    service = services.Services()
    template = loader.get_template('index.html')
    bestseries = service.discover_best_series()
    context = {'bestseries' : bestseries}
    return HttpResponse(template.render(context = context))