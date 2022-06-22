from django.db import models
from django.contrib.auth.models import User


class UserData(User):
    otp = models.IntegerField(default=000000, max_length=6)
    pass
