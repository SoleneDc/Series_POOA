
url_discover_key = "https://api.themoviedb.org/3/discover/tv?api_key=e4c6a6f5fbd60b0316b7ff30e73bec74&language=en-US&sort_by=popularity.desc"


req = requests.get(url_discover_key)
pprint(req.json())


class Services:
    url = "https://api.themoviedb.org/3/"
    key = "e4c6a6f5fbd60b0316b7ff30e73bec74"

    def SearchByName(self,name):
        """TODO : fonction qui affiche les résultats d'une recherche"""

    def researchPerson(self,Person):
        """
        Returns XXX to check
        """



    def effacerFavori(self, user):
        """TODO : fonction qui efface les favori d'un user"""

