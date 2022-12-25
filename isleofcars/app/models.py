from django.contrib.auth.models import User
from django.db import models


class Ad(models.Model):
    id = models.AutoField(primary_key=True)
    make = models.CharField(max_length=255, null=True, blank=True)
    model = models.CharField(max_length=255, null=True, blank=True)
    year = models.IntegerField(null=True, blank=True)
    price = models.FloatField(null=True, blank=True)
    source = models.CharField(max_length=255, null=True, blank=True)
    source_url = models.CharField(max_length=1024, null=True, blank=True)
    url = models.CharField(max_length=255, null=True, blank=True)
    is_new = models.BooleanField(null=True, blank=True)
    is_broken = models.BooleanField(null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    photos = models.JSONField(null=True, blank=True, default=list)
    title = models.CharField(max_length=255, null=True, blank=True)
    body = models.CharField(max_length=255, null=True, blank=True)
    mileage = models.FloatField(null=True, blank=True)
    transmission = models.CharField(max_length=255, null=True, blank=True)
    drive = models.CharField(max_length=255, null=True, blank=True)
    power = models.FloatField(null=True, blank=True)
    color = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    favored_by = models.ManyToManyField(User, through='FavoriteAd')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='author', null=True, blank=True)
    objects = models.Manager()

    def __str__(self):
        return (f'{self.__class__.__name__}: {self.make} {self.model} '
                f'(id={self.id})')

    class Meta:
        db_table = 'ad'
        managed = True
        ordering = ('-id',)


class FavoriteAd(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
    objects = models.Manager()

    class Meta:
        db_table = 'ad_favored_by'
        managed = True
        ordering = ('-id',)

#
# class Favorite(models.Model):
#     id = models.AutoField(primary_key=True)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
#     added = models.DateTimeField(auto_now_add=True)
#     objects = models.Manager()
#
#     class Meta:
#         db_table = 'favorite'
#         managed = True
#         ordering = ('-id',)
