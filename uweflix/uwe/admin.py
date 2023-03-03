from django.contrib import admin
from uweflix.settings import AUTH_USER_MODEL
from .models import Users

# Register your models here.
admin.site.register(Users)
