from django.contrib import admin

# Register your models here.
from .models import UserProfile, Town

admin.site.register(UserProfile)
admin.site.register(Town)
