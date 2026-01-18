from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("hobbies",views.hobbies,name="hobbies"),
    path("hobbies/<int:hobby_id>/", views.hobby, name="hobby"),
    path("user/<int:user_id>/", views.user, name="user"),
    path("vote/<int:hobby_id>", views.vote, name="vote"),
    path("add_offering/", views.add_offering, name="add_offering"),
]
