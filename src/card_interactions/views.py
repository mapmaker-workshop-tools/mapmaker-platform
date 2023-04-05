
# Create your views here.
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import condition
from workshop.models import Card
from django.utils import timezone
from users.models import CustomUser
from .forms import CardForm, CARD_TYPE_CHOICES, CardTitle, CardDescription, CardResource, CardComment
from .models import Follower, Resource, Comment
from django.contrib import messages
from emailhandler.standard_emails import standard_email, notify_followers_new_post
from core.utils import mp, signer

def validate_user_access_to_card(id, request):
    card = Card.objects.get(id=id)
    if request.user in card.workshop.participants.all():
        print(True)
    else:
        print(False)

def get_card_details(request, id):
    card = Card.objects.get(id=id)
    current_user = request.user
    workshop = card.workshop.id
    workshop_secret = signer.sign_object({'workshopid':workshop})
    resources = Resource.objects.filter(card=card)
    comments = Comment.objects.filter(card=card)
    followers = Follower.objects.filter(card_liked=id)
    followerIDlist = []
    for i in followers:
        followerIDlist.append(i.user_like)
    followers = CustomUser.objects.filter(email__in=followerIDlist)
    user_follows_card = current_user in followerIDlist
    form = CardComment()
    context = {
        'cardtype': card.cardtype,
        'author': card.author,
        'title': card.title,
        'type': card.cardtype,
        'description': card.description,
        'followers': followers,
        'id': card.id,        
        'user_follows_card': user_follows_card,
        'resources': resources,
        'comments': comments,
        'form': form,
        'workshop_secret': workshop_secret
    }
    try:
        mp.track(request.user.email, 'Viewed card', {
        'card title': card.title,
        'card id': card.id,
        'card id': card.id,
        'workshop': card.workshop.workshop_name, 
        'anonymous': False,
        'HTTP_USER_AGENT': request.META['HTTP_USER_AGENT'],
        })
    except:
        mp.track('Anonymous', 'Viewed card', {
        'card title': card.title,
        'card id': card.id,
        'card id': card.id,
        'workshop': card.workshop.workshop_name, 
        'anonymous': True,
        'HTTP_USER_AGENT': request.META['HTTP_USER_AGENT'],
        })
    return render(request, 'drawer.html', context)
 
@login_required   
def create_card(request, id):
    card = Card.objects.get(id=id)
    current_user = request.user
    resources = Resource.objects.filter(card=card)
    comments = Comment.objects.filter(card=card)
    followers = Follower.objects.filter(card_liked=id)
    followerIDlist = []
    for i in followers:
        followerIDlist.append(i.user_like)
    followers = CustomUser.objects.filter(email__in=followerIDlist)
    user_follows_card = current_user in followerIDlist
    form = CardComment()
    context = {
        'cardtype': card.cardtype,
        'author': request.user,
        'title': 'New Card',
        'type': card.cardtype,
        'description': "Add a new description",
        'followers': followers,
        'id': card.id,        
        'user_follows_card': user_follows_card,
        'resources': resources,
        'comments': comments,
        'form': form
    }
    mp.track(request.user.email, 'Card created', {
    'card title': card.title,
    'card id': card.id,
    'workshop': card.workshop.workshop_name,
    
    'HTTP_USER_AGENT': request.META['HTTP_USER_AGENT'],
    
    })
    return render(request, 'drawer.html', context)

@login_required
def edit_card_title(request, id):
    card = Card.objects.get(id=id)
    if request.method == 'POST':
        form = CardTitle(request.POST)
        if form.is_valid():
            card.title = form.cleaned_data['title']
            card.cardtype = CARD_TYPE_CHOICES[int(form.cleaned_data['cardtype'])-1][1]
            card.author = request.user
            card.save()
            messages.add_message(request, messages.INFO, 'Card title updated')
            mp.track(request.user.email, 'Card title updated', {
            'card title': card.title,
            'card id': card.id,
            'workshop': card.workshop.workshop_name,
            
            'HTTP_USER_AGENT': request.META['HTTP_USER_AGENT'],
            
            })
            return render(request, 'new_title.html', {"title":form.cleaned_data['title'], "id":id, "type":card.cardtype})
    else: 
        form = CardTitle()
    return render(request, 'edit_title.html', {'form': form, "cardid": id ,"title":card.title, "type":card.cardtype})

@login_required
def edit_card_description(request, id):
    if request.method == 'POST':
        form = CardDescription(request.POST)
        if form.is_valid():
            card = Card.objects.get(id=id)
            card.description = form.cleaned_data['description']
            card.save()
            mp.track(request.user.email, 'Card description updated', {
            'card title': card.title,
            'card id': card.id,
            'workshop': card.workshop.workshop_name,
            
            'HTTP_USER_AGENT': request.META['HTTP_USER_AGENT'],
            
            
            })
            messages.add_message(request, messages.INFO, 'Card description updated')
            return render(request, 'new_description.html', {"description" : form.cleaned_data['description'], "id" : id})
    else: 
        form = CardDescription()
        card = Card.objects.get(id=id)
        description = card.description
    return render(request, 'edit_description.html', {'form': form, "cardid": id, "description":description})

@login_required
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
            return render(request, 'notliked.html', {"id":id})
        else:
            card = Card.objects.get(id=id)
            new_like = Follower(user_like=current_user, card_liked=card)
            new_like.save()
            mp.track(request.user.email, 'Card followed', {
            'card title': card.title,
            'card id': card.id,
            'workshop': card.workshop.workshop_name,
            
            'HTTP_USER_AGENT': request.META['HTTP_USER_AGENT'],
                       
            })
            messages.add_message(request, messages.INFO, 'You followed card' +card.title)
            return render(request, 'liked.html', {"id":id})
@login_required   
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
        mp.track(request.user.email, 'Card deleted', {
        'card title': card.title,
        'card id': card.id,
        'workshop': card.workshop.workshop_name,
        
        'HTTP_USER_AGENT': request.META['HTTP_USER_AGENT'],
        
            
        })
        messages.add_message(request, messages.INFO, 'Card deleted')
        clear_card(id)
        return render(request, 'empty.html')

@login_required
def create_resource(request, id):
    if request.method == 'POST':
        form = CardResource(request.POST)
        if form.is_valid():
            card = Card.objects.get(id=id)
            resource = Resource(
                owner = request.user,
                card = card,
                document_description = form.cleaned_data['description'],
                document_type = 'Link',
                document_url = form.cleaned_data['url'],
                date_modified = timezone.now
            )
            mp.track(request.user.email, 'Resource created', {
            'card title': card.title,
            'card id': card.id,
            'resource id': resource.id,
            'workshop': card.workshop.workshop_name,
            
            'HTTP_USER_AGENT': request.META['HTTP_USER_AGENT'],
            
            })
            resource.save()
            comment = Comment(
                card = card,
                comment_text = 'Added resource ' + str(resource.document_description),
                author = request.user,
            )
            comment.save()
            return redirect('/dashboard')
        else:
            return HttpResponse(status=404)
    else:
        form = CardResource()
        return render(request, 'create_resource.html', {'form': form, "cardid": id})

@login_required
def create_comment(request, id, notify):
    if request.method == 'POST':
        card = Card.objects.get(id=id)
        form = CardComment(request.POST)
        if form.data['comment_text'] == '':
            return HttpResponse(status=204)
        else:
            new_comment = Comment(
                    card = card,
                    comment_text = form.data['comment_text'],
                    author = request.user,
                    )
            new_comment.save()
            mp.track(request.user.email, 'Comment created', {
            'card title': card.title,
            'card id': card.id,
            'comment id': new_comment.id,
            'workshop': card.workshop.workshop_name,
            
            'HTTP_USER_AGENT': request.META['HTTP_USER_AGENT'],
            
            
            })
            comments = Comment.objects.filter(card=card)
            if notify == 'yes':
                notify_followers_new_post(id)
                mp.track(request.user.email, 'Comment notification sent', {
                'card title': card.title,
                'card id': card.id,
                'comment id': new_comment.id,
                'workshop': card.workshop.workshop_name,
                'comment': new_comment.comment_text,
                
                'HTTP_USER_AGENT': request.META['HTTP_USER_AGENT'],
                
                
                })
            return render(request, 'comment.html', {'comments': comments})
    else:
        return HttpResponse(status=404)

@login_required
def delete_comment(request, id, comment_id):
    if request.method == 'DELETE':
        card = Card.objects.get(id=id)
        comment_delete = Comment.objects.get(id=comment_id)
        mp.track(request.user.email, 'Comment deleted', {
            'card title': card.title,
            'workshop': card.workshop.workshop_name,
            'comment': comment_delete.comment_text,
            'comment': comment_delete.id,
            
            'HTTP_USER_AGENT': request.META['HTTP_USER_AGENT'],
            
            })
        comments = Comment.objects.filter(card=card)
        comments = comments.order_by('date_created')
        comment_delete.delete()
        return render(request, 'comment.html', {'comments': comments, 'id':id})

@login_required
def delete_resource(request, id, resource_id):
    if request.method == 'DELETE':
        card = Card.objects.get(id=id)
        resource_delete = Resource.objects.get(id=resource_id)
        mp.track(request.user.email, 'Resource deleted', {
            'card title': card.title,
            'workshop': card.workshop.workshop_name,
            'resource description': resource_delete.document_description,
            'resource id': resource_delete.id,
            
            'HTTP_USER_AGENT': request.META['HTTP_USER_AGENT'],
            
            })
        resource_delete.delete()
        resources = Resource.objects.filter(card=card)
        return render(request, 'resources.html', {'resources': resources, 'id':id})

def clear_card(id):
    card = Card.objects.get(id=id)
    followers = Follower.objects.filter(card_liked=card)
    comments = Comment.objects.filter(card=card)
    resources = Resource.objects.filter(card=card)
    followers.delete()
    comments.delete()
    resources.delete()
    