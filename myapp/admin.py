from django.contrib import admin
from django.contrib.auth.models import User

# Register your models here.

from .models import AuthProfile

admin.site.register(AuthProfile)
# User.objects.all()
