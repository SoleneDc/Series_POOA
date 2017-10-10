class User:
    """This class represent the user of our app"""

    def __init__(self, id, firstName, lastName, birthDate, gender, picture, favoriteSeries):
        """Basic constructor"""
        self._id = id
        self.first_name = firstName
        self.last_name = lastName
        self.birth_date = birthDate
        self.gender = gender
        self.picture = picture
        self.favoriteSeries = favoriteSeries

    def _get_id(self):
        """Getter for the id"""
        return self._id

    def _set_id(self, id):
        """Setter for the id"""
        print("Sorry but the id is definitive.")

    #Like that the id cannot be changed
    id = property(_get_id, _set_id)

