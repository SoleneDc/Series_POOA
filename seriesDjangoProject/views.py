import json
import requests
from django.contrib.auth import *
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from seriesDjangoProject import services, exception
from .forms import *

"""This class defines the controllers for the application
each fonction is supposed to process a page and send it to the url mapper"""


def index(request):
    try:
        service = services.Services()
        template = loader.get_template('index.html')
        bestseries = service.discover_best_series() # c'est censé être une liste d'objets
        user = service.getFullUserFromRequest(request)
        request.user=user
        favoriteListe = service.getFavoritesOfUser(user)
        context = {'bestseries' : bestseries, 'favoriteListe': favoriteListe}
        return HttpResponse(template.render(request=request, context=context))
    except requests.ConnectionError:
        template = loader.get_template('error.html')
        context = {'message': "We were unable to connect to the API...",
                   'todo': "You can check your internet connection!"}
        return HttpResponse(template.render(request=request, context=context))


def search(request):
    try:
        # if this is a POST request we need to process the form data
        if request.method == 'POST':
            # create a form instance and populate it with data from the request:
            form = SearchForm(request.POST)
            # check whether it's valid:
            #hello
            if form.is_valid():

                if request.POST.get('tick')=="series":
                    service = services.Services()  # charge service
                    template = loader.get_template('searchResult.html')  # charge la page html
                    # request.POST['search'] est la chaine de caractères entrée en recherche par l'user
                    serie_id = service.get_IDs(
                        request.POST['search']) # effectue la recherche et récupère l'ID
                    user = service.getFullUserFromRequest(request)
                    response = []
                    for i in range(0,len(serie_id)):
                            serie = service.get_serie(serie_id[i])
                            response.append(serie)
                    response = service.joinInfoAboutFavoriteToSerieList(response, user)
                    response = service.joinInfoAboutComingEpisode(response)
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

        # if a GET (or any other method) we'll create a blank form//
        else:
            form = SearchForm()
            return render(request, 'index.html', {'form': form})
    except exception.InputError:
        template = loader.get_template('error.html')
        context = {'message': "You must enter only alphanumerical values...",'todo':"Refresh the page to try again!"}
        return HttpResponse(template.render(request=request, context=context))
    except requests.ConnectionError:
        template = loader.get_template('error.html')
        context = {'message': "We were unable to connect to the API...",'todo':"You can check your internet connection!"}
        return HttpResponse(template.render(request=request, context=context))


def signIn(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = RegisterForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            if User.objects.filter(username =form.data['username']).exists()==False:
                json_response = {'status': 'OK'}
                # process the data in form.cleaned_data as required
                # ...
                # redirect to a new URL:*
                user = User.objects.create_user(form.data['username'], form.data['email'], form.data['password'])
                user.save()
                context = {'name': user.username}
                return HttpResponse(json.dumps(json_response), content_type='application/json')
            else:
                json_response = {'status': 'KO'}
                return HttpResponse(json.dumps(json_response), content_type='application/json')
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
        user ={'id' : user.id}
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


def addToFavorites(request, id):
    try:
        service = services.Services()
        serie = service.get_serie(id)
        user = service.getFullUserFromRequest(request)
        result = service.addToFavorites(user, serie)
        json_response = {'status': result}
        return HttpResponse(json.dumps(json_response), content_type='application/json')
    except requests.ConnectionError:
        template = loader.get_template('error.html')
        context = {'message': "We were unable to connect to the API...",
                   'todo': "You can check your internet connection!"}
        return HttpResponse(template.render(request=request, context=context))


def removeFromFavorites(request, id):
    try:
        service = services.Services()
        serie = service.get_serie(id)
        user = service.getFullUserFromRequest(request)
        result = service.removeFromFavorites(user, serie)
        json_response = {'status': result}
        return HttpResponse(json.dumps(json_response), content_type='application/json')
    except requests.ConnectionError:
        template = loader.get_template('error.html')
        context = {'message': "We were unable to connect to the API...",
                   'todo': "You can check your internet connection!"}
        return HttpResponse(template.render(request=request, context=context))


def getSeriesInformation(request, series_id):
    """
    Function used when we click on a picture
    """
    try:
        service = services.Services()
        user = service.getFullUserFromRequest(request)
        series = service.get_serie(series_id)
        template = loader.get_template('searchResult.html')
        response = []
        response.append(series)
        response = service.joinInfoAboutFavoriteToSerieList(response, user)
        response = service.joinInfoAboutComingEpisode(response)
        context = {'response': response}
        return HttpResponse(template.render(request=request, context=context))
    except requests.ConnectionError:
        template = loader.get_template('error.html')
        context = {'message': "We were unable to connect to the API...",
                   'todo': "You can check your internet connection!"}
        return HttpResponse(template.render(request=request, context=context))