from django.db import models
from uweflix.settings import AUTH_USER_MODEL
from django.contrib.auth.models import AbstractUser
# Create your models here.

# class Users(AbstractUser):
#     is_accountManager = models.BooleanField('Is account manager', default=False)
#     is_clubRepresentative = models.BooleanField('Is club representative', default=False)
#     is_customer = models.BooleanField('Is customer', default=False)
#     is_cinemaManager = models.BooleanField('Is cinema manager', default=False)