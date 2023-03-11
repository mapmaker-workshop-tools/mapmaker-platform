
# Create your views here.
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from workshop.models import Card
from django.utils import timezone
from users.models import CustomUser
from .forms import CardForm, CARD_TYPE_CHOICES, CardTitle, CardDescription
from .models import Follower
from django.contrib import messages


    
def get_card_details(request, id):
    card = Card.objects.get(id=id)
    current_user = request.user
    followers = Follower.objects.filter(card_liked=id)
    followerIDlist = []
    for i in followers:
        followerIDlist.append(i.user_like)
    followers = CustomUser.objects.filter(email__in=followerIDlist)
    user_follows_card = current_user in followerIDlist
    context = {
        'cardtype': card.cardtype,
        'author': card.author,
        'title': card.title,
        'description': card.description,
        'followers': followers,
        'id': card.id,        
        'user_follows_card':user_follows_card
    }
    return render(request, 'drawer.html', context)
    
def create_card(request, id):
    if request.method == 'POST':
        current_user = request.user
        form = CardForm(request.POST)
        if form.is_valid():
            card = Card.objects.get(id=id)
            card.description = form.cleaned_data['description']
            card.title = form.cleaned_data['title']
            card.date_modified = timezone.now
            card.cardtype = CARD_TYPE_CHOICES[int(form.cleaned_data['cardtype'])-1][1]
            card.author = current_user
            card.save()
            messages.add_message(request, messages.INFO, 'Card Created')
            return redirect('/dashboard')
    else: 
        form = CardForm()
    return render(request, 'create_card.html', {'form': form, "cardid": id})

def edit_card_title(request, id):
    if request.method == 'POST':
        form = CardTitle(request.POST)
        if form.is_valid():
            card = Card.objects.get(id=id)
            card.title = form.cleaned_data['title']
            card.save()
            messages.add_message(request, messages.INFO, 'Card title updated')
            return render(request, 'new_title.html', {"title":form.cleaned_data['title'], "id":id})
    else: 
        form = CardTitle()
    return render(request, 'edit_title.html', {'form': form, "cardid": id})


def edit_card_description(request, id):
    if request.method == 'POST':
        form = CardDescription(request.POST)
        if form.is_valid():
            card = Card.objects.get(id=id)
            card.description = form.cleaned_data['description']
            card.save()
            messages.add_message(request, messages.INFO, 'Card description updated')
            return render(request, 'new_description.html', {"description" : form.cleaned_data['description'], "id" : id})
    else: 
        form = CardDescription()
        card = Card.objects.get(id=id)
        description = card.description
    return render(request, 'edit_description.html', {'form': form, "cardid": id, "description":description})

def register_like(request, id):
    current_user = request.user
    cardid = id
    ## If this card exists
    if not Card.objects.filter(pk=id).exists():
        return HttpResponse(status=404)
    else:
    ## Check if a like exists by our user
        like = Follower.objects.filter(card_liked = id)
        like = like.filter(user_like = current_user)
    # Delete the like 
        if like.exists(): 
            like.delete()
            print("like deleted")
            return render(request, 'notliked.html', {"id":id})
        else:
            card = Card.objects.get(id=id)
            new_like = Follower(user_like=current_user, card_liked=card)
            new_like.save()
            messages.add_message(request, messages.INFO, 'You followed card' +card.title)
            return render(request, 'liked.html', {"id":id})
    
def delete_card(request, id):
    ## If this card exists
    if not Card.objects.filter(pk=id).exists():
        return HttpResponse(status=404)
    else:
        #We don't actually delete the card but set it to "empty and blank"""
        card = Card.objects.get(id=id)
        card.title = 'empty'
        card.description = 'empty'
        card.cardtype = 'empty'
        card.author = CustomUser(pk=5)
        card.save()
        messages.add_message(request, messages.INFO, 'Card deleted')
        return render(request, 'empty.html')
    