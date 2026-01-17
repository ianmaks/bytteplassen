import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.template import loader

from .models import Hobby, Vote


# Create your views here.
def index(request):
    all_hobbies = Hobby.objects.order_by("-votes")
    template = loader.get_template("marketplace/index.html")
    context = {"all_hobbies": all_hobbies}
    return HttpResponse(template.render(context, request))


def hobby(request, hobby_id):
    user_id = request.user.id
    hobby = Hobby.objects.get(id=hobby_id)
    has_voted = Vote.objects.filter(user_id=user_id, hobby_id=hobby_id).exists()

    template = loader.get_template("marketplace/hobby.html")
    context = {
        "hobby": hobby,
        "voted": 1 if has_voted else 0,
    }
    return HttpResponse(template.render(context, request))


def vote(request):
    vote_action = request.POST.get("vote")
    user_id = request.POST.get("user")
    hobby_id = request.POST.get("hobby")

    if vote_action == 1:
        vote = Vote(hobby=hobby_id, user=user_id)
        vote.save()
        return HttpResponse("Vote cast!")
    elif vote_action == 0:
        Vote.objects.delete(hobby=hobby_id, user=user_id)
        return HttpResponse("Vote removed!")
    else:
        return HttpResponse("Vote rejected!")


def user(request, user_id):
    return HttpResponse("You're looking at this user")
