from django.db import models


class UserData(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField(null=False, max_length=100)
    password = models.CharField(null=False, max_length=512)

    def __str__(self):
        return self.username
