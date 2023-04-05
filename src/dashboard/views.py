
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
from django.http import HttpResponse
from .utils import create_image
from workshop.models import Card
from core.utils import mp, signer



@login_required
def index(request):
    if request.user.is_authenticated:
        # Getting the user, active workshop cards and participants
        current_user = request.user
        current_workshop = current_user.active_workshop
        workshop_secret = signer.sign_object({'workshopid':current_workshop.id})
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
                "zoomlevel": str(current_user.zoom_level),
                "workshop_secret": workshop_secret,
                "participantcount": participants.count()}
        mp.track(request.user.email, 'Dashboard loaded ', {'workshop': current_workshop.workshop_name, 'anonymous': False,
    'HTTP_USER_AGENT': request.META['HTTP_USER_AGENT'], })
        return render(request, 'dashboard_index.html', context)
    else:
        return redirect('/user/login')
    
    
def view_only(request, workshop_secret):
    if request.user.is_authenticated:
        return redirect('/dashboard')
    else:
        # Getting the live workshop from the secret 
        workshopid_unsigned = int(signer.unsign_object(workshop_secret)['workshopid'])
        current_workshop = Workshop.objects.get(id=workshopid_unsigned)  
        cards = Card.objects.filter(workshop=current_workshop)
        participants = Workshop.participants.through.objects.filter(workshop=current_workshop)
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
                "firstname": 'Anonymous',
                'cards': ordered_cards, 
                "participants": participants, 
                "workshop": current_workshop,
                "ambitioncount": cards.filter(cardtype='ambition').count(),
                "ideacount": cards.filter(workshop=current_workshop).filter(cardtype='idea').count(), 
                "challengecount": cards.filter(workshop=current_workshop).filter(cardtype='challenge').count(),  
                "cardscount": cards.count(), 
                "zoomlevel": '0',
                "workshop_secret": workshop_secret,
                "participantcount": participants.count()}
        mp.track('Anonymous', 'Dashboard loaded ', {'workshop': current_workshop.workshop_name, 'anonymous': True,
    'HTTP_USER_AGENT': request.META['HTTP_USER_AGENT'], })
        return render(request, 'dashboard_index.html', context)
    
@login_required
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
        mp.track(request.user.email, 'Moved card', {'workshop': current_workshop.workshop_name, 
    'HTTP_USER_AGENT': request.META['HTTP_USER_AGENT'], })
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
        if current_user.zoom_level == '0':
            return render(request, 'grid_zoom_standard.html', context)
        elif current_user.zoom_level == '1':
            return render(request, 'grid_zoom_out.html', context)
        elif current_user.zoom_level == '2':
            return render(request, 'grid_zoom_in.html', context)
    else:
        return HttpResponse(status=403)

def close(request):
    return render(request, 'empty.html')

@login_required
def zoom_in(request):
    print("Zoom in hit")
    user = request.user
    t = CustomUser.objects.get(id=user.id)
    zoom_level = user.zoom_level
    if zoom_level == '0':
        t.zoom_level = '2'
        t.save() 
    elif zoom_level == '1':
        t.zoom_level = '0'
        t.save() 
    current_workshop = user.active_workshop
    cards = Card.objects.filter(workshop=current_workshop)
    if not current_workshop.card_order:
        ordered_cards = cards
    else:
        get_card_order_list = ast.literal_eval(current_workshop.card_order)
        order_cards = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(get_card_order_list)])
        ordered_cards = cards.filter(pk__in=get_card_order_list).order_by(order_cards)
    context = {'cards': ordered_cards, 'zoomlevel': t.zoom_level}
    mp.track(request.user.email, 'Zoom in', {'workshop': current_workshop.workshop_name, 
    'HTTP_USER_AGENT': request.META['HTTP_USER_AGENT'],})
    return render(request, 'adjust_zoom.html', context)

@login_required
def zoom_out(request):
    print("Zoom out hit")
    user = request.user
    t = CustomUser.objects.get(id=user.id)
    zoom_level = user.zoom_level
    if zoom_level == '0':
        t.zoom_level = '1'
        t.save() 
    elif zoom_level == '1':
        pass
    else:
        t.zoom_level = '0'
        t.save() 
    current_workshop = user.active_workshop
    cards = Card.objects.filter(workshop=current_workshop)
    if not current_workshop.card_order:
        ordered_cards = cards
    else:
        get_card_order_list = ast.literal_eval(current_workshop.card_order)
        order_cards = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(get_card_order_list)])
        ordered_cards = cards.filter(pk__in=get_card_order_list).order_by(order_cards)
    context = {'cards': ordered_cards, 'zoomlevel': t.zoom_level}
    mp.track(request.user.email, 'Zoom out', {'workshop': current_workshop.workshop_name, 
    'HTTP_USER_AGENT': request.META['HTTP_USER_AGENT'],})
    return render(request, 'adjust_zoom.html', context)

@login_required
def download_image(request):
    workshop = request.user.active_workshop.workshop_name
    #Putting a template together with the information of the usersession
    template = index(request)
    data = {'html': template, 'render_when_ready':True, 'ms_delay':1000}
    image_url = create_image(data)
    mp.track(request.user.email, 'Workshop image downloaded', {'workshop': workshop, 
    'HTTP_USER_AGENT': request.META['HTTP_USER_AGENT'],})
    return redirect(image_url)