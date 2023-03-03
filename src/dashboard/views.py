
# Create your views here.
from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from workshop.models import Workshop, Card
from users.models import CustomUser
from card_interactions.models import Like, Comment
from django.db import models
import re



#@login_required
def index(request):
    if request.user.is_authenticated:
        current_user = request.user #Getting currentuser
        current_workshop = current_user.active_workshop   #Setting the workshop to a known value from the usersettings. If the user has more workshops they can toggle. 
        #Get some workshop data for dashboard
        cards = Card.objects.filter(workshop=current_workshop)
        cardcount = cards.count()
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
        context = {"firstname": current_username, 'cards':cards, "participants":participants, "workshop": current_workshop,"ambitioncount":ambitioncount,"ideacount":ideacount, "challengecount":challengecount,  "cardscount":cardcount, "participantcount":participantcount}
        return render(request, 'dashboard_index.html', context)
    else:
        return redirect('/admin/')
    
def handle_network_update(request):
    response = request.body.decode("utf-8")
    list_of_nodes_ordered = re.findall(r'\d+', response)
    print(list_of_nodes_ordered)
    return HttpResponse(status=204)