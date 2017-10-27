from django.db import models

class User(models.Model):
    """This class represent the user of our app"""

    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField()
    birth_date = models.DateField()
    gender = models.CharField(max_length=1)
    #picture

    def __init__(self, id):
        """Ce constructeur"""

