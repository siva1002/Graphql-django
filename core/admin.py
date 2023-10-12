from django.contrib import admin
from django.contrib.auth.models import Permission
from .models import Musician,Album

admin.site.register(Musician)
admin.site.register(Permission)

# Register your models here.
