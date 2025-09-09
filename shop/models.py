from django.db import models
from django.contrib.auth.models import User


class Coffees(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, null=False, blank=False)
    name = models.CharField(max_length=250, null=False, blank=False)
    description = models.TextField(null=False, blank=False)
    picture = models.ImageField(
        upload_to='pictures/coffees', null=False, blank=False)
