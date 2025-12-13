from django.contrib import admin

from .models import User, Hobby, UserHasHobby

admin.site.register(User)
admin.site.register(Hobby)
admin.site.register(UserHasHobby)
