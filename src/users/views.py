from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import CustomUserLoginForm, CustomUserProfile, CustomUserRegisterToWorkshop
from users.models import CustomUser
from card_interactions.models import Card, Follower, Comment, Resource
from datetime import datetime
from workshop.models import Workshop
from core.utils import mp, signer
from emailhandler.standard_emails import welcome_new_user

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
            mp.track(user.email, 'Logged in' , {'HTTP_USER_AGENT': request.META['HTTP_USER_AGENT'],} )
            mp.people_set(user.email, {
            '$last_login'    : datetime.now(),})
            return redirect('/dashboard')
        else:
            messages.add_message(request, messages.INFO, 'Invalid username or password')
            return redirect('/user/login')
    else:
        form = CustomUserLoginForm()
        return render(request, 'login.html', {'form':form})
    
def logout_view(request):
    mp.track(request.user.email, 'Log out', {
    'HTTP_USER_AGENT': request.META['HTTP_USER_AGENT'],})
    logout(request)
    messages.add_message(request, messages.INFO, 'Logged out')
    return redirect('/')

def register(request, workshop_secret):
    workshopid_unsigned = int(signer.unsign_object(workshop_secret)['workshopid'])
    workshop = Workshop.objects.get(id=workshopid_unsigned)    
    if request.method == "POST":
        form = CustomUserRegisterToWorkshop(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            repeat_password = form.cleaned_data['repeat_password']
            organisation = form.cleaned_data['organisation']
            if password != repeat_password:
                messages.add_message(request, messages.INFO, 'Passwords do not match')
                return redirect('/user/register/'+workshop_secret)
            if CustomUser.objects.filter(email=email).exists():
                messages.add_message(request, messages.INFO, 'You already have an account, please login or reset your password')
                mp.track(email, 'User tried to register with existing account' , {'HTTP_USER_AGENT': request.META['HTTP_USER_AGENT'],} )
                return redirect('/user/login')
            new_user = CustomUser(
                email = email,
                organisation = organisation,
                active_workshop = workshop
            )
            new_user.set_password(password)
            new_user.save()
            workshop.participants.add(new_user)
            new_user = authenticate(request, username=email, password=password)
            welcome_new_user(email, workshop.workshop_name)
            login(request, new_user)
            mp.track(email, 'New user registered' , {'HTTP_USER_AGENT': request.META['HTTP_USER_AGENT'],} )
            mp.people_set(email, {
            '$last_login'    : datetime.now(),})
            return redirect('/dashboard')
        else:
            messages.add_message(request, messages.INFO, 'Invalid username or password')
            return redirect('/user/login')
    else:
        if request.user.is_authenticated:
            return redirect('/dashboard')
        else:
            form = CustomUserRegisterToWorkshop()
            return render(request, 'register.html', {'form':form, 'workshop':workshop, 'workshop_secret':workshop_secret})



def profile(request):
    user = request.user
    workshop = user.active_workshop
    cardcount = Card.objects.filter(author=user).count()
    commentcount = Comment.objects.filter(author=user).count()
    resourcecount = Resource.objects.filter(owner=user).count()
    likecount = Follower.objects.filter(user_like=user).count()
    form = CustomUserLoginForm()
    mp.track(user.email, 'User profile', {
    'HTTP_USER_AGENT': request.META['HTTP_USER_AGENT'],})
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
            mp.track(user.email, 'User profile updated', {
    'HTTP_USER_AGENT': request.META['HTTP_USER_AGENT'],})
            #return redirect('/user/profile')
            return render(request, 'user_profile_table.html')
        elif request.method == 'GET':
            user = request.user
            workshops = Workshop.objects.filter(participants__email=user.email)
            context = {'workshops': workshops}
            return render(request, 'user_profile_table_edit.html', context)
    else: 
        return HttpResponse(status=403)
    
def delete_user(request, id):
    ## If this user exists
    if not CustomUser.objects.filter(pk=id).exists():
        return HttpResponse(status=404)
    else:       
        user = CustomUser.objects.get(id=id)
        mp.track(user.email, 'User deleted', {
        'user': user.email,
        'HTTP_USER_AGENT': request.META['HTTP_USER_AGENT'],
        })
        mp.people_delete(user.email, {})
        logout(request)
        user.delete()
        print("BUTTON HIT")
        return redirect('/')