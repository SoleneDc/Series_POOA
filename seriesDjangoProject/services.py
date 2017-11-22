import requests
from datetime import datetime
from seriesDjangoProject import exception
from seriesDjangoProject.models.class_series import Serie
from seriesDjangoProject.models.series_user import SeriesUser
from django.contrib.auth.models import User



class Services:
    #si les constantes ne sont utilisées que dans une classe précise, il faut les passer en mode privé avec __devant
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

    def test(query):
        """
        :param query: Corresponding to the user's search
        :return: Returns False if the user typed weird symbols
        """
        answer = True
        for symb in query:
            if symb.isalnum() == False and symb != "'" and symb != "!":
                answer = False
        return answer

    def get_IDs(self, query):
        """
        :param query: Corresponding to the user's search
        :return: Returns a list of the series' ids (corresponding to the user's search)
        """
        url_final = Services.URL_BASE + Services.SEARCH + Services.KEY + '&query=' + query
        if Services.test(query) == False:
            raise exception.InputError(query,"There is an issue with your query")
        else:
            req = requests.get(url_final)
            result = []
            for item in req.json()['results']:
                result.append(item['id'])
            return result

    def get_serie(self, id_serie):
        """
        :param id_serie: ID of the series
        :return: Returns the object serie corresponding to the ID
        """
        url_final = Services.URL_BASE + Services.GET_TV + str(id_serie) + '?' + Services.KEY
        req = requests.get(url_final)
        x = Serie(req.json())
        return x

    def coming_episode(self, id_serie, L):
        """
        :param id_serie: ID of the series
        :param L: The length of the list represents the number of seasons // excluding the specials
        :return: a dictionary where key = series ID and value = episode if there is an episode is coming in less than 7 days, {} if not
        """
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
        :param query: = the user's search (it should be a person)
        :return: list of celebrities corresponding to the search
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
        :return: Function that gives the user the 20 most popular series (there are 20 series displayed by page)
        """
        url_final = Services.URL_BASE + Services.DISCOVER + Services.KEY + '&sort_by=popularity.desc&page=1&include_null_first_air_dates=false'
        req = requests.get(url_final)
        list_best_series = []
        for item in req.json()['results']:
            x = Serie(item)
            list_best_series.append(x)
        return list_best_series

    def removeFromFavorites(self, user, serie):
        """
        :param user: the user
        :param serie: a serie
        :return: Removes the serie from the user's favorites
        """
        if user.is_anonymous:
            raise exception.AuthenticationException
        else:
           SeriesUser.objects.filter(user_id=user.id, serie_id=serie.id).delete()
        return 'OK'

    def addToFavorites(self, user, serie):
        """
        :param user: the user
        :param serie: a serie
        :return: Adds the serie from the user's favorites
        """
        if user.is_anonymous:
            raise exception.AuthenticationExeption
        else:
            newEntry=SeriesUser(user_id=user.id,serie_id=serie.id)
            newEntry.save()
            return 'OK'

    def joinInfoAboutFavoriteToSerieList(self, series, user):
        """
        :param user: the user
        :param series: list of series
        :return: Adds to each series an attribute for it to be in the user's favorite or not
        """
        result = []
        if user is None:
            for serie in series:
                serie.isFavorite = False
                serie.user_logged_in = False
            return series
        for serie in series:
            if SeriesUser.objects.filter(user_id=user.id, serie_id=serie.id).all().__len__()>=1:
                serie.isFavorite = True
            else:
                serie.isFavorite = False
            serie.user_logged_in = True
            result.append(serie)
        return result

    def joinInfoAboutComingEpisode(self, series_list):
        """
        :param series_list: list of series
        :return: Adds to the series the following attributes is_coming_soon (if an episode is released in less than 7 days), episode_coming_soon_name,
        episode_coming_soon_air_date
        """
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
                    else:
                        series.is_netflix = False
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
        """
        :param request:
        :return: The user if he is logged in
        """
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
        Return the list of series that the user favorites"""
        if user is None:
           result=None
        else:
            result=[]
            correspondanceList = SeriesUser.objects.filter(user_id=user.id).all()
            for correspondance in correspondanceList:
                serie = self.get_serie(correspondance.serie_id)
                result.append(serie)
        return result