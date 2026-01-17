import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.template import loader
from django.views.decorators.csrf import csrf_protect
from .models import Hobby, Vote
from django.db.models import Count



# Create your views here.
def index(request):
    all_hobbies = Hobby.objects.annotate(vote_count=Count('votes')).order_by("-vote_count")
    template = loader.get_template("marketplace/index.html")
    context = {"all_hobbies": all_hobbies}
    return HttpResponse(template.render(context, request))


def hobby(request, hobby_id):
    user_id = request.user.id
    hobby = Hobby.objects.get(id=hobby_id)
    has_voted = Vote.objects.filter(user_id=user_id, hobby_id=hobby_id).exists()
    votes = hobby.votes.count()

    template = loader.get_template("marketplace/hobby.html")
    context = {
        "hobby": hobby,
        "voted": 1 if has_voted else 0,
        "votes": votes
    }
    return HttpResponse(template.render(context, request))

@csrf_protect
def vote(request, hobby_id):
    if request.method != "POST":
        return HttpResponse("Invalid request method", status=405)
    
    vote_action = request.POST.get("vote")
    user = request.user
    hobby = Hobby.objects.get(id=hobby_id)
    
    if hobby:
        if vote_action == "1":
            vote = Vote(hobby=hobby, user=user)
            vote.save()
            return HttpResponse("Vote cast!")
        elif vote_action == "0":
            Vote.objects.filter(hobby=hobby, user=user).delete()
            return HttpResponse("Vote removed!")
        else:
            return HttpResponse("Vote rejected!")


def user(request, user_id):
    return HttpResponse("You're looking at this user")
