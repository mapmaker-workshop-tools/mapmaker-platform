from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import CustomUserLoginForm, CustomUserProfile
from users.models import CustomUser
from card_interactions.models import Card, Follower, Comment, Resource
from datetime import datetime
from workshop.models import Workshop
from core.utils import mp


# Create your views here.
def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            user.last_login = datetime.now()
            user.save() 
            messages.add_message(request, messages.INFO, 'welcome back ' + user.first_name)
            mp.track(user.email, 'Logged in')
            return redirect('/dashboard')
        else:
            messages.add_message(request, messages.INFO, 'Invalid username or password')
            return redirect('/user/login')
    else:
        form = CustomUserLoginForm()
        return render(request, 'login.html', {'form':form})
    
def logout_view(request):
    mp.track(request.user.email, 'Logged out')
    logout(request)
    messages.add_message(request, messages.INFO, 'Logged out')
    return redirect('/')

def register(request):
    return render(request, 'register.html')

def profile(request):
    user = request.user
    workshop = user.active_workshop
    cardcount = Card.objects.filter(author=user).count()
    commentcount = Comment.objects.filter(author=user).count()
    resourcecount = Resource.objects.filter(owner=user).count()
    likecount = Follower.objects.filter(user_like=user).count()
    form = CustomUserLoginForm()
    mp.track(user.email, 'User profile')
    return render(request, 'userprofile.html', {'user': user,'cardcount':cardcount,'likecount':likecount, 'resourcecount':resourcecount, 'commentcount':commentcount, 'form':CustomUserProfile, 'workshop':workshop})

def profile_edit(request, id):
    if request.user.id == id:    
        if request.method == 'POST':
            firstname = request.POST['firstName']
            lastname = request.POST['lastname']
            email = request.POST['email']
            organisation = request.POST['organisation']
            linkedin = request.POST['linkedin']
            active_workshop = request.POST['default-radio']
            messages.add_message(request, messages.INFO, 'Updated profile')
            workshop = Workshop.objects.get(id=int(request.POST['default-radio']))
            t = CustomUser.objects.get(id=id)
            t.first_name = firstname
            t.active_workshop = workshop
            t.last_name = lastname
            t.email = email
            t.linkedin = linkedin
            t.save()
            mp.track(user.email, 'User profile updated')
            #return redirect('/user/profile')
            return render(request, 'user_profile_table.html')
        elif request.method == 'GET':
            user = request.user
            workshops = Workshop.objects.filter(participants__email=user.email)
            context = {'workshops': workshops}
            return render(request, 'user_profile_table_edit.html', context)
    else: 
        return HttpResponse(status=403)