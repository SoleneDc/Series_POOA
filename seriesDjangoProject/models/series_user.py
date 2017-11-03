from django.db import models
class SeriesUser(models.Model):
    """This class links a user to his series"""
    user_id = models.IntegerField()
    serie_id = models.IntegerField()