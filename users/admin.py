from django.contrib import admin

from users.models import User, Location

admin.site.register(Location)
admin.site.register(User)
