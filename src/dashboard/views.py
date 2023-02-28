
# Create your views here.
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from workshop.models import Workshop, Card
from users.models import CustomUser
from card_interactions.models import Like, Comment
from django.db import models
import json
from random import randrange

grid = [[0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0]]

card_type_options = ['ambition', 'challenge', 'idea', 'pro', 'con']

def calculate_network(workshop_id):
    workshop = Workshop.objects.get(pk=workshop_id)
    cardsinworkshop = Card.objects.filter(workshop=workshop)
    networkdata = []
    for card in cardsinworkshop:
        parent = Card.objects.get(pk=card.parentnode)
        networkdata.append([card.title, parent.title])
    return json.dumps(networkdata)

def calculate_honeycomb(workshop_id):
    workshop = Workshop.objects.get(pk=workshop_id)
    cardsinworkshop = Card.objects.filter(workshop=workshop)
    honeycombdata = []
    print(grid)
    for card in cardsinworkshop:
        offset = 1
        parent = Card.objects.get(pk=card.parentnode)
        print(parent)
        x = randrange(9)
        y = randrange(9)
        """
        if any(parent in y for x in grid):
            print('Found in grid')
            print(parent)"""
        new_node = {
            "hc-a2": str(card.id),
            "name": card.title +' Name',
            "region": card.title +' Name',
            "x": x,
            "y": y,
            "value":card_type_options.index(card.cardtype)
            }
        grid[x][y] = card.id
        honeycombdata.append(new_node)
    print(grid)
    return json.dumps(honeycombdata)



#@login_required
def index(request):
    current_user = request.user #Getting currentuser
    current_workshop = current_user.active_workshop   #Setting the workshop to a known value from the usersettings. If the user has more workshops they can toggle. 
    #Get some workshop data for dashboard
    cardcount = Card.objects.filter(workshop=current_workshop).count()
    ambitioncount = Card.objects.filter(workshop=current_workshop).filter(cardtype='ambition').count()
    challengecount = Card.objects.filter(workshop=current_workshop).filter(cardtype='challenge').count()
    ideacount = Card.objects.filter(workshop=current_workshop).filter(cardtype='idea').count()
    #Getting all participants for this workshop
    participants = Workshop.participants.through.objects.filter(workshop=current_workshop)
    participantcount = participants.count()
    userIDlist = []
    current_username = current_user.first_name
    for i in participants:
        userIDlist.append(i.customuser_id)
    participants = CustomUser.objects.filter(pk__in=userIDlist)
    #Getting the network data so we can draw it
    networkdata = calculate_network(current_workshop.id)
    honeycombdata = calculate_honeycomb(current_workshop.id)
    #Sending context and rendering dashboard
    context = {"firstname": current_username, "participants":participants,"honeycombdata":honeycombdata, "networkdata": networkdata, "workshop": current_workshop,"ambitioncount":ambitioncount,"ideacount":ideacount, "challengecount":challengecount,  "cardscount":cardcount, "participantcount":participantcount}
    return render(request, 'dashboard_index.html', context)