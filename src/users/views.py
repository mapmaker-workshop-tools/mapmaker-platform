from datetime import datetime, timedelta

from card_interactions.models import Card, Comment, Follower, Resource
from core.utils import mp, signer
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponse, redirect, render
from emailhandler.standard_emails import welcome_new_user
from workshop.models import Workshop
from core.settings import ENVIRONMENT
from users.models import CustomUser

from .forms import CustomUserLoginForm, CustomUserProfile, CustomUserRegisterToWorkshop


# Create your views here.
def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            user.last_login = datetime.now()
            user.save()
            messages.add_message(request, messages.INFO, "welcome back " + user.first_name)
            mp.track(user.email, "Logged in", {"environment": ENVIRONMENT})
            mp.people_set(user.email, {
                "$last_login": datetime.now()})
            return redirect("/dashboard")
        else:
            messages.add_message(request, messages.INFO, "Invalid username or password")
            return redirect("/user/login")
    else:
        form = CustomUserLoginForm()
        return render(request, "login.html", {"form": form})


@login_required
def logout_view(request):
    mp.track(request.user.email, "Log out", {"environment": ENVIRONMENT,
        "HTTP_USER_AGENT": request.META["HTTP_USER_AGENT"]})
    logout(request)
    messages.add_message(request, messages.INFO, "Logged out")
    return redirect("/")


def register(request, workshop_secret):
    try:
        signer.unsign_object(workshop_secret, max_age=timedelta(days = 7))
        pass
    except:
        return render(request, "expired.html")
    workshopid_unsigned = int(signer.unsign_object(workshop_secret)["workshopid"])
    workshop = Workshop.objects.get(id=workshopid_unsigned)
    if request.method == "POST":
        form = CustomUserRegisterToWorkshop(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            repeat_password = form.cleaned_data["repeat_password"]
            organisation = form.cleaned_data["organisation"]
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            if password != repeat_password:
                messages.add_message(request, messages.INFO, "Passwords do not match")
                return redirect("/user/register/"+workshop_secret)
            if CustomUser.objects.filter(email=email).exists():
                messages.add_message(request, messages.INFO, "You already have an account, please login or reset your password")
                mp.track(email, "User tried to register with existing account" , {"environment": ENVIRONMENT} )
                return redirect("/user/login")
            new_user = CustomUser(
                email = email,
                organisation = organisation,
                active_workshop = workshop,
                first_name = first_name,
                last_name = last_name,
            )
            new_user.set_password(password)
            new_user.save()
            workshop.participants.add(new_user)
            new_user = authenticate(request, username=email, password=password)
            welcome_new_user(email, workshop.workshop_name)
            login(request, new_user)
            mp.track(email, "New user registered" , {"environment": ENVIRONMENT,} )
            mp.people_set(email, {
            "$last_login"    : datetime.now()})
            return redirect("/dashboard")
        else:
            messages.add_message(request, messages.INFO, "Invalid username or password")
            return redirect("/user/login")
    else:
        if request.user.is_authenticated:
            return redirect("/dashboard")
        else:
            form = CustomUserRegisterToWorkshop()
            return render(request, "register.html", {"form":form, "workshop":workshop, "workshop_secret":workshop_secret})


@login_required
def profile(request):
    user = request.user
    workshop = user.active_workshop
    cardcount = Card.objects.filter(author=user).count()
    commentcount = Comment.objects.filter(author=user).count()
    resourcecount = Resource.objects.filter(owner=user).count()
    likecount = Follower.objects.filter(user_like=user).count()
    CustomUserLoginForm()
    mp.track(user.email, "User profile", {"environment": ENVIRONMENT,
    "HTTP_USER_AGENT": request.META["HTTP_USER_AGENT"]})
    return render(request, "userprofile.html",
                {"user": user,
                "cardcount":cardcount,
                "likecount":likecount,
                "resourcecount":resourcecount,
                "commentcount":commentcount,
                "form":CustomUserProfile,
                "workshop":workshop})

@login_required
def profile_edit(request, id):
    user = request.user
    workshops = Workshop.objects.filter(participants__email=user.email)
    context = {"workshops": workshops, "user":user}
    if request.user.id == id:
        if request.method == "POST":
            firstname = request.POST["firstName"]
            lastname = request.POST["lastname"]
            email = request.POST["email"]
            organisation = request.POST["organisation"]
            linkedin = request.POST["linkedin"]
            messages.add_message(request, messages.INFO, "Updated profile")
            t = CustomUser.objects.get(id=id)
            t.first_name = firstname
            t.last_name = lastname
            t.email = email
            t.linkedin = linkedin
            t.organisation = organisation
            t.save()
            user = CustomUser.objects.get(email=email)
            mp.track(email, "User profile updated", {"environment": ENVIRONMENT,
    "HTTP_USER_AGENT": request.META["HTTP_USER_AGENT"]})
            return render(request, "user_profile_table.html", {"workshops": workshops, "user":user})
        elif request.method == "GET":
            return render(request, "user_profile_table_edit.html", context)
        return None
    else:
        return HttpResponse(status=403)

    
@login_required
def profile_edit_upload_image(request, id):
    user = request.user
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        t = CustomUser.objects.get(email=user.email)
        t.avatar = myfile
        t.save()
        return redirect("/user/profile")
    else:
        return render(request, "upload_image.html", {"user":user})

@login_required
def delete_user(request, id):
    ## If this user exists
    if not CustomUser.objects.filter(pk=id).exists():
        return HttpResponse(status=404)
    else:
        user = CustomUser.objects.get(id=id)
        mp.track(user.email, "User deleted", {
        "user": user.email,
        "environment": ENVIRONMENT,
        })
        mp.people_delete(user.email, {})
        logout(request)
        user.delete()
        return redirect("/")
