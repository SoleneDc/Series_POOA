import requests
from seriesDjangoProject.models.class_series import Serie
from collections import namedtuple
from datetime import datetime, date, timedelta
from pprint import pprint


class Services:
    URL_BASE = "https://api.themoviedb.org/3/"
    KEY = "api_key=e4c6a6f5fbd60b0316b7ff30e73bec74"
    SEARCH = 'search/tv?'
    SEARCHPEOPLE = 'search/person?'
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



    def effacerFavori(self, user):
        """TODO : fonction qui efface les favoris d'un user"""


