from django.db import models
from member.models import User

class RestaurantInfo1(models.Model):
    name = models.CharField(max_length=255, null=False)
    bookmark_count = models.IntegerField(default=0)
    icon_path = models.CharField(max_length=255)
    latitude = models.FloatField(null=False, default =0.0)
    longitude = models.FloatField(null=False, default =0.0)

class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.ForeignKey(RestaurantInfo1, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'name')


