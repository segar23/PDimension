from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=250, unique=True)
    isMacro = models.BooleanField(default=False)
