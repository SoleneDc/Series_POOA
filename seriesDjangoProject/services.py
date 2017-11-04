import requests
from seriesDjangoProject import exception
from seriesDjangoProject.models.class_series import Serie
from seriesDjangoProject.models.series_user import SeriesUser
from django.contrib.auth.models import User


class Services:
    URL_BASE = "https://api.themoviedb.org/3/"
    KEY = "api_key=e4c6a6f5fbd60b0316b7ff30e73bec74"
    SEARCH = 'search/tv?'
    SEARCHPEOPLE = 'search/person?'
    GET_TV = 'tv/'
    DISCOVER = 'discover/tv?'
    FIND = 'find/tv?'
    CHARMED_TVID = 1981 #information given for testing
    TIMEZONE = 'FR'

    def __init__(self):
        pass

    def search_series_names(self, query):
        """
        Function that searches the Series by name and returns all the Series names that include the string in input
        """
        url_final = Services.URL_BASE + Services.SEARCH + Services.KEY + '&query=' + query
        req = requests.get(url_final)
        result = []
        for item in req.json()['results']:
            x = Serie(item)
            result.append(x)
        return result

    def get_serie(self, query):

        url_final = Services.URL_BASE + Services.GET_TV + str(query) + '?' + Services.KEY
        req = requests.get(url_final)
        x = Serie(req.json())

        return x

    def get_IDs(self, query):

        url_final = Services.URL_BASE + Services.SEARCH + Services.KEY + '&query=' + query
        req = requests.get(url_final)
        result = []
        for item in req.json()['results']:
            result.append(item['id'])
        return result

    def search_people(self, query):
        """
        Returns XXX to check
        """
        url_final = Services.URL_BASE + Services.SEARCHPEOPLE + Services.KEY + '&query=' + query
        req = requests.get(url_final)
        result = []
        print (req.json())
        for item in req.json()['results']:
            result.append(item['name'])
        return result

    def discover_best_series(self):
        """
        Function that gives the user the 20 most popular series (there are 20 series displayed by page)
        """
        url_final = Services.URL_BASE + Services.DISCOVER + Services.KEY + '&sort_by=popularity.desc&page=1&include_null_first_air_dates=false'
        req = requests.get(url_final)
        result = []
        for item in req.json()['results']:
            result.append(item['name'])
        return result

    def discover_series_on_the_air(self):
        """
        Functions that returns a list of 20 most popular series on the air within the next 7 days, sorted by popularity
        """
        url_final = Services.URL_BASE + 'tv/on_the_air?' + Services.KEY + '&page=1'
        req = requests.get(url_final)
        result = []
        for item in req.json()['results']:
            result.append(item['name'])
        return result

    def get_genres(self):
        """
        Function that returns the list of series genres available on TMDB. It allows us to stay up-to-date about all the genres they list.
        """
        url_final = Services.URL_BASE + 'genre/tv/list?' + Services.KEY
        req = requests.get(url_final)
        result = {}
        for item in req.json()['genres']:
            result[item['id']] = item['name']
        return result

    def removeFromFavorites(self, user, serie):
        if user.is_anonymous:
            raise exception.AuthenticationException
        else:
           SeriesUser.objects.filter(user_id=user.id, serie_id=serie.id).delete()
        return 'OK'

    def addToFavorites(self, user, serie):
        if user.is_anonymous:
            raise exception.AuthenticationExeption
        else:
            newEntry=SeriesUser(user_id=user.id,serie_id=serie.id)
            newEntry.save()
            return 'OK'

    def joinInfoAboutFavoriteToSerieList(self, series, user_id):
        result = []
        for serie in series:
            if SeriesUser.objects.filter(user_id=user_id, serie_id=serie.id).all().__len__()>=1:
                serie.isFavorite=True
            result.append(serie)
        return result

    def getFullUserFromRequest(self,request):
        """This fonction return the user if he is logged in"""
        if 'user' in request.session._session:
            user = request.session._session['user'] #Dictionnary object with only id and name
            user_id = user['id']
            full_user = User.objects.get(id=user_id)
            return full_user
        else:
            return None

    def getFavoritesOfUser(self, user):
        """We cannnot adapt the user class since it is define by Django, so it goes into a service
        Returnth list of series that the user favorites"""
        if user is None:
           result=None
        else:
            result=[]
            correspondaceList = SeriesUser.objects.filter(user_id=user.id).all()
            for correspondance in correspondaceList:
                serie = self.get_serie(correspondance.serie_id)
                result.append(serie)
        return result