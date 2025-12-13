from django.shortcuts import render
from django.http import HttpResponse
from .models import Hobby


# Create your views here.
def index(request):
    all_hobbies = Hobby.objects.order_by("-votes")
    output = ",\n ".join([f"{h.name} {h.hobby_output} {h.votes}" for h in all_hobbies])
    return HttpResponse(output)


def hobby(request, hobby_id):
    return HttpResponse("You're looking at this hobby: ")


def user(request, user_id):
    return HttpResponse("You're looking at this user")
