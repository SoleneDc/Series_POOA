# Find here the class Series and maybe the class Review if found useful.


import requests
from datetime import datetime, date, timedelta
from pprint import pprint

url = "https://api.themoviedb.org/3/"
url_discover_key = "https://api.themoviedb.org/3/discover/tv?api_key=e4c6a6f5fbd60b0316b7ff30e73bec74&language=en-US&sort_by=popularity.desc"
key = "e4c6a6f5fbd60b0316b7ff30e73bec74"

req = requests.get(url_discover_key)
pprint(req.json())


class Serie:
    def __init__(self, id,  episode_run_time, first_air_date, genres, in_production, languages, last_air_date, name,
                 networks, episodes, seasons, origin_country, original_language, original_name,
                 overview, popularity, production_companies, vote_avg, vote_count):
        self.id = id
        self.episode_run_time = episode_run_time
        self.first_air_date = first_air_date
        self.genres = genres
        self.in_production = in_production
        self.languages = languages
        self.last_air_date = last_air_date
        self.name = name
        self.networks = networks
        self.episodes = episodes
        self.seasons = seasons
        self.origin_country = origin_country
        self.original_language = original_language
        self.original_name = original_name
        self.overview = overview
        self.popularity = popularity
        self.production_companies = production_companies
        self.vote_avg = vote_avg
        self.vote_count = vote_count


class Season:
    def __init__(self, id, air_date, episodes, name, overview, season_number):
        self.id = id
        self.air_date = air_date
        self.episodes = episodes
        self.name = name
        self.overview = overview
        self.season_number = season_number


class Episode:
    def __init__(self, id, air_date, episode_number, name, overview, season_number, vote_avg, vote_count):
        self.id = id
        self.air_date = air_date
        self.episode_number = episode_number
        self.name = name
        self.overview = overview
        self.season_number = season_number
        self.vote_avg = vote_avg
        self.vote_count = vote_count




