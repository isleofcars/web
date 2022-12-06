from django.db import models
from django.contrib.auth.models import User

from app.models import CarAdvertisement


class Favorite(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    ads_id = models.ManyToManyField('app.CarAdvertisement')

    class Meta:
        db_table = 'ads_favorite'    # table name in the remote db