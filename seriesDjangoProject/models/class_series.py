# Find here the class Series and maybe the class Review if found useful.


from django.db import models

url = "https://api.themoviedb.org/3/"
url_discover_key = "https://api.themoviedb.org/3/discover/tv?api_key=e4c6a6f5fbd60b0316b7ff30e73bec74&language=en-US&sort_by=popularity.desc"
key = "e4c6a6f5fbd60b0316b7ff30e73bec74"

#req = requests.get(url_discover_key)
#pprint(req.json())


class Serie():
    """Class defining a Series"""
    def __init__(self, dict):
        for k,v in dict.items():
            setattr(self, k, v)



# Series Getter :
    @property
    def tv_id(self):
        return self._tv_id

    @property
    def genres(self):
        return self._genres

    @property
    def name(self):
        return self._name

    @property
    def episodes(self):
        return self._episodes

    @property
    def seasons(self):
        return self._seasons

    @property
    def overview(self):
        return self._overview

    @property
    def popularity(self):
        return self._popularity

    @property
    def vote_avg(self):
        return self._vote_avg

    @property
    def vote_count(self):
        return self._vote_count

# Series Setter :
    @tv_id.setter
    def tv_id(self, value):
        self._tv_id = value

    @genres.setter
    def genres(self, value):
        self._genres = value

    @name.setter
    def name(self, value):
        self._name = value

    @episodes.setter
    def episodes(self, value):
        self._episodes = value

    @seasons.setter
    def seasons(self, value):
        self._seasons = value

    @overview.setter
    def overview(self, value):
        self._overview = value

    @popularity.setter
    def popularity(self, value):
        self._popularity = value

    @vote_avg.setter
    def vote_avg(self, value):
        self._vote_avg = value

    @vote_count.setter
    def vote_count(self, value):
        self._vote_count = value




    def __get__(self, instance, owner):
        '''TODO'''

    def __set__(self, instance, value):
        '''TODO'''


class Season:
    '''Class defining a Season'''
    def __init__(self, id, air_date, episodes, name, overview, season_number):
        self.id = id
        self.air_date = air_date
        self.episodes = episodes
        self.name = name
        self.overview = overview
        self.season_number = season_number


#en fait on utilise pas ca :
    def __get__(self, instance, owner):
        '''TODO'''

    def __set__(self, instance, value):
        '''TODO'''


class Episode:
    '''Class defining an Episode'''
    def __init__(self, id, air_date, episode_number, name, overview, season_number, vote_avg, vote_count):
        self.id = id
        self.air_date = air_date
        self.episode_number = episode_number
        self.name = name
        self.overview = overview
        self.season_number = season_number
        self.vote_avg = vote_avg
        self.vote_count = vote_count

    def __get__(self, instance, owner):
        '''TODO'''

    def __set__(self, instance, value):
        '''TODO'''