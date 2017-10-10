class Person:
    def __init__(self, last_name, first_name, gender, birthday, deathday):

        # Propriétés
        self.last_name = last_name
        self.first_name = first_name
        self.gender = gender
        self.birthday = birthday
        self.deathday = deathday


class Actor (Person):
    def __init__(self, last_name, first_name, gender, birthday, biography, deathday, popularity):
        Person.__init__(self, last_name, first_name, gender, birthday, biography, deathday, popularity)
        self.biography = biography
        self.popularity = popularity

class Staff (Person):
    def __init__(self, last_name, first_name, gender, birthday, biography, deathday, popularity, job, series):
        Person.__init__(self, last_name, first_name, gender, birthday, biography, deathday, popularity, job, series)
        self.job = job
        self.series = series



