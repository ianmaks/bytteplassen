from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("hobbies/<int:hobby_id>/", views.hobby, name="hobby"),
    path("user/<int:user_id>/", views.user, name="user"),
    path("vote/", views.vote, name="vote"),
]
