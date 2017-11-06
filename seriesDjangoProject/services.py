import requests
from datetime import datetime
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
    GET_SEASON = '/season/'
    DISCOVER = 'discover/tv?'
    FIND = 'find/tv?'
    CHARMED_TVID = 1981  # information given for testing
    TIMEZONE = 'FR'

    def __init__(self):
        pass

    def get_IDs(self, query):
        url_final = Services.URL_BASE + Services.SEARCH + Services.KEY + '&query=' + query
        req = requests.get(url_final)
        result = []
        for item in req.json()['results']:
            result.append(item['id'])
        return result

    def get_serie(self, id_serie):
        url_final = Services.URL_BASE + Services.GET_TV + str(id_serie) + '?' + Services.KEY
        req = requests.get(url_final)
        x = Serie(req.json())
        return x

    def coming_episode(self, id_serie, L):
        L2 = L
        while len(L2) != 0:
            num_season = len(L2)
            url_final = Services.URL_BASE + Services.GET_TV + str(id_serie) + Services.GET_SEASON + str(num_season) + '?' + Services.KEY
            req = requests.get(url_final)
            season = req.json()
            today = datetime.now()
            if season['air_date'] == None:
                return {id_serie: {}}
            date_first_episode = datetime.strptime(season['air_date'], "%Y-%m-%d")
            result = []
            if (today - date_first_episode).days > 0 and (today - date_first_episode).days < 365 :
                for episode in season['episodes']:
                    date_episode = datetime.strptime(episode['air_date'], "%Y-%m-%d")
                    if date_episode > today:
                        if (date_episode - today).days <= 7:
                            return {id_serie: episode}
            else:
                L2=L2[1:]
            return {id_serie: {}}

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

    def joinInfoAboutFavoriteToSerieList(self, series, user):
        result = []
        if user is None:
            return series
        for serie in series:
            if SeriesUser.objects.filter(user_id=user.id, serie_id=serie.id).all().__len__()>=1:
                serie.isFavorite=True
            result.append(serie)
        return result

    def joinInfoAboutComingEpisode(self, series_list):
        result = []
        for series in series_list:
            L=[]
            episode = {}
            if series.status == 'Returning Series':
                if len(series._seasons) == 1:
                    L = [0]
                else:
                    L = [0] * (len(series._seasons) - 1)  # il existe une saison 0 pour les 'specials' que nous ne prenons pas en compte ici
                episode = self.coming_episode(series.id, L)
                if episode[series.id] == {}:
                    if series.networks != [] and series.networks[0]['name']=='Netflix':
                        series.is_netflix = True
                    series.is_coming_soon = False
                else:
                    series.is_coming_soon = True
                    series.episode_coming_soon_name = episode[series.id]['name']
                    series.episode_coming_soon_air_date = episode[series.id]['air_date']
            else:
                series.is_coming_soon = False
            result.append(series)
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

    def weekly_mail(self, user):
        """Create the weekly mail for a user"""
        seriesList = self.getFavoritesOfUser(user)
        if seriesList.__len__()==0:
            return None
        else:
            for series in seriesList:
                print("Mail about this serie for user :" +user.username)

    def getFavoritesOfUser(self, user):
        """We cannnot adapt the user class since it is define by Django, so it goes into a service
        Returnth list of series that the user favorites"""
        if user is None:
           result=None
        else:
            result=[]
            correspondanceList = SeriesUser.objects.filter(user_id=user.id).all()
            for correspondance in correspondanceList:
                serie = self.get_serie(correspondance.serie_id)
                result.append(serie)
        return result