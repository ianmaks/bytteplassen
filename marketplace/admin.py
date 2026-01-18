from django.contrib import admin

from .models import User, Hobby, UserHasHobby, Offering

admin.site.register(User)
admin.site.register(Hobby)
admin.site.register(UserHasHobby)
admin.site.register(Offering)
