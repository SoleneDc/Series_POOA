import requests
from seriesDjangoProject import exception
from seriesDjangoProject.models.class_series import Serie
from seriesDjangoProject.models.series_user import SeriesUser


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
        """?"""
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

    def remove_from_favorites(self, user, serie):
        if user.is_anonymous:
            raise exception.AuthenticationException
        else:
           SeriesUser.objects.filter(user_id=user.id, serie_id=serie.id).delete()
        return 'OK'

    def add_to_favorites(self, user, serie):
        if user.is_anonymous:
            raise exception.AuthenticationExeption
        else:
            newEntry = SeriesUser(user_id=user.id,serie_id=serie.id)
            newEntry.save()
            return 'OK'

    def join_info_about_favorite_to_serie_list(self, series, user_id):
        result = []
        for serie in series:
            if SeriesUser.objects.filter(user_id=user_id, serie_id=serie.id).all().__len__()>=1:
                serie.isFavorite = True
            result.append(serie)
        return result

    #ne marche pas trop...
    def get_favorite_series_id(self, user_id):
        """
        Function that returns a list of series given an ID
        """
        result = SeriesUser.objects.filter(user_id = user_id)
        url_final = Services.URL_BASE + Services.GET_TV + '{tv_id}?' + Services.KEY
        return result


Services().get_favorite_series_id('Pauline')