import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.template import loader
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from .models import Hobby, Vote, Offering, Trade
from .forms import OfferingForm, TradeForm
from django.db.models import Count, Case, When, Value, IntegerField



# Create your views here.
def index(request):
    all_offerings = Offering.objects.annotate(
        priority=Case(
            When(stock_status__in=['I', 'D'], then=Value(1)),
            When(stock_status='O', then=Value(2)),
            default=Value(1),
            output_field=IntegerField()
        ),
        vote_count=Count('hobby__votes')
    ).order_by('priority', '-vote_count')
    template = loader.get_template("marketplace/index.html")
    context = {"all_offerings": all_offerings}
    return HttpResponse(template.render(context, request))

def hobbies(request):
    all_hobbies = Hobby.objects.annotate(vote_count=Count('votes')).order_by("-vote_count")
    template = loader.get_template("marketplace/hobbies.html")
    context = {"all_hobbies": all_hobbies}
    return HttpResponse(template.render(context, request))


def hobby(request, hobby_id):
    user_id = request.user.id
    hobby = Hobby.objects.get(id=hobby_id)
    has_voted = Vote.objects.filter(user_id=user_id, hobby_id=hobby_id).exists()
    votes = hobby.votes.count()
    related_offerings = Offering.objects.filter(hobby=hobby)
    template = loader.get_template("marketplace/hobby.html")
    context = {
        "hobby"     : hobby,
        "voted"     : 1 if has_voted else 0,
        "votes"     : votes,
        "offerings" : related_offerings
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

def add_offering(request):
    if request.method == 'POST':
        form = OfferingForm(request.POST)
        if form.is_valid():
            offering = form.save(commit=False)
            offering.owner = request.user
            offering.save()
            return redirect('index')
    else:
        form = OfferingForm()
    template = loader.get_template("marketplace/add_offering.html")
    context = {'form': form}
    return HttpResponse(template.render(context, request))

def offering_detail(request, offering_id):
    offering = Offering.objects.get(id=offering_id)
    is_owner = offering.owner == request.user
    
    if request.method == 'POST':
        if is_owner:
            if 'update_stock' in request.POST:
                offering.stock_status = request.POST.get('stock_status')
                offering.save()
                return redirect('offering_detail', offering_id=offering_id)
            elif 'delete' in request.POST:
                offering.delete()
                return redirect('index')
            elif 'respond_trade' in request.POST:
                trade_id = request.POST.get('trade_id')
                action = request.POST.get('action')
                trade = Trade.objects.get(id=trade_id)
                if action == 'accept':
                    trade.status = 'A'
                    messages.success(request, f'Trade from {trade.proposer.username} accepted!')
                elif action == 'reject':
                    trade.status = 'R'
                    messages.info(request, f'Trade from {trade.proposer.username} rejected.')
                elif action == 'too_low':
                    trade.status = 'T'
                    messages.info(request, f'Trade from {trade.proposer.username} marked as too low.')
                trade.save()
                return redirect('offering_detail', offering_id=offering_id)
        else:
            if 'update_my_trade' in request.POST:
                trade_id = request.POST.get('my_trade_id')
                quantity = request.POST.get('quantity')
                trade = Trade.objects.get(id=trade_id, proposer=request.user)
                trade.quantity = quantity
                trade.save()
                return redirect('offering_detail', offering_id=offering_id)
            elif 'delete_my_trade' in request.POST:
                trade_id = request.POST.get('my_trade_id')
                Trade.objects.filter(id=trade_id, proposer=request.user).delete()
                return redirect('offering_detail', offering_id=offering_id)
            else:
                form = TradeForm(request.POST, user=request.user)
                if form.is_valid():
                    trade = form.save(commit=False)
                    trade.target_offering = offering
                    trade.proposer = request.user
                    trade.save()
                    return redirect('offering_detail', offering_id=offering_id)
    
    pending_trades = offering.incoming_trades.filter(status='P') if is_owner else None
    accepted_trades = offering.incoming_trades.filter(status='A') if is_owner else None
    rejected_trades = offering.incoming_trades.filter(status__in=['R', 'T']) if is_owner else None
    trade_form = TradeForm(user=request.user) if not is_owner else None
    my_trades = offering.incoming_trades.filter(proposer=request.user) if not is_owner and request.user.is_authenticated else None

    template = loader.get_template("marketplace/offering_detail.html")
    context = {
        'offering': offering,
        'is_owner': is_owner,
        'pending_trades': pending_trades,
        'accepted_trades': accepted_trades,
        'rejected_trades': rejected_trades,
        'trade_form': trade_form,
        'my_trades': my_trades,
    }
    return HttpResponse(template.render(context, request))