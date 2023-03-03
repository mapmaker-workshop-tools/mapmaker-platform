
# Create your views here.
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from workshop.models import Workshop, Card
from users.models import CustomUser
from card_interactions.models import Like, Comment
from django.db import models
import json
from random import randrange

def find_location(x,y, cardtype):
    position = cardtype
    if position == 0:
        return x-1, y+1
    elif position == 1:
        return x, y+1
    elif position == 2:
        return x+1, y+1
    elif position == 3:
        return x-1, y
    elif position == 4:
        return x+1, y
    elif position == 5:
        return x-1, y-1
    elif position == 6:
        return x, y-1
    elif position == 7:
        return x+1, y-1
    

##PSEUDOCODE: 
# Loop over all cards to find parent
# parent is where the id of the node == as parent.id (It's pointing at itself)
# loop over all children for that node and place them alongside
# If it does not fit try again


card_type_options = ['ambition', 'challenge', 'idea', 'pro', 'con', 'add', 'remove']

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
    for card in cardsinworkshop:
        parent = Card.objects.get(pk=card.parentnode)
        parent_x = int(parent.x_location)
        parent_y = int(parent.y_location)
        if card.id == parent.id:
            x = parent_x
            y = parent_y
        else:
            x,y = find_location(parent_x,parent_y, card_type_options.index(card.cardtype))
        new_node = {
            "hc-a2": str(card.title),
            "name": card.title,
            "region": card.title,
            "x": x,
            "y": y,
            "value":card_type_options.index(card.cardtype)
            }
        honeycombdata.append(new_node)
    return json.dumps(honeycombdata)

#@login_required
def index(request):
    if request.user.is_authenticated:
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
    else:
        return render(request, 'login.html')