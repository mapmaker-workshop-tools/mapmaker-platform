
# Create your views here.
from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from workshop.models import Workshop, Card
from django.utils import timezone
from users.models import CustomUser
from django.db import models
from django.db.models import Case, When
import json
import ast
import re



#@login_required
def index(request):
    if request.user.is_authenticated:
        # Getting the user, active workshop cards and participants
        current_user = request.user
        current_workshop = current_user.active_workshop
        cards = Card.objects.filter(workshop=current_workshop)
        participants = Workshop.participants.through.objects.filter(workshop=current_workshop)
        # Here we fetch and order the cards in this workshop 
        if not current_workshop.card_order:
            ordered_cards = cards
        else:
            get_card_order_list = ast.literal_eval(current_workshop.card_order)
            order_cards = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(get_card_order_list)])
            ordered_cards = cards.filter(pk__in=get_card_order_list).order_by(order_cards)
        # Doing a lookup of all participants in this workshop
        userIDlist = []
        for i in participants:
            userIDlist.append(i.customuser_id)
        #Get all the participants to this session --> This ensures we can query their details in templates
        participants = CustomUser.objects.filter(pk__in=userIDlist)
        context = {
                "firstname": current_user.first_name,
                'cards': ordered_cards, 
                "participants": participants, 
                "workshop": current_workshop,
                "ambitioncount": cards.filter(cardtype='ambition').count(),
                "ideacount": cards.filter(workshop=current_workshop).filter(cardtype='idea').count(), 
                "challengecount": cards.filter(workshop=current_workshop).filter(cardtype='challenge').count(),  
                "cardscount": cards.count(), 
                "participantcount": participants.count()}
        return render(request, 'dashboard_index.html', context)
    else:
        return redirect('/admin/')
    

def handle_grid_update(request):
    if request.method == "POST":
        current_user = request.user
        current_workshop = current_user.active_workshop
        response = request.body.decode("utf-8")
        list_of_nodes_ordered = re.findall(r'\d+', response)
        jsonStr = json.dumps(list_of_nodes_ordered)
        t = Workshop.objects.get(id=current_workshop.id)
        t.card_order = jsonStr
        t.save() 
        return HttpResponse(status=204)
    elif request.method == "GET":
        current_user = request.user
        current_workshop = current_user.active_workshop
        cards = Card.objects.filter(workshop=current_workshop)
        if not current_workshop.card_order:
            ordered_cards = cards
        else:
            get_card_order_list = ast.literal_eval(current_workshop.card_order)
            order_cards = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(get_card_order_list)])
            ordered_cards = cards.filter(pk__in=get_card_order_list).order_by(order_cards)
        context = {'cards': ordered_cards }
        return render(request, 'grid.html', context)
    else:
        return HttpResponse(status=403)

def close(request):
    print("Card Closed")
    return render(request, 'empty.html')