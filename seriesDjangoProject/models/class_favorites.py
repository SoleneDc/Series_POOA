from django.db import models
from seriesDjangoProject.models import class_user

class Favorites(models.Model):
    """This class represent the user of our app"""
    id_user = models.ForeignKey(class_user.User, on_delete=models.CASCADE)
    id_serie =models.DecimalField()
