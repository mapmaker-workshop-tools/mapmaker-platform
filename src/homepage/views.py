from core.utils import mp
from django.contrib import messages
from django.shortcuts import redirect, render
from django.utils import timezone
from emailhandler.standard_emails import confirm_new_order, welcome_new_marketing_lead

from .forms import EmailMarketing, Orderform
from .models import EmailList, Order
from core.settings import ENVIRONMENT


# Create your views here.
def index(request):
    if request.method == "POST":
        form = EmailMarketing(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            new_marketing_lead = EmailList(
                email = email,
            )
            new_marketing_lead.save()
            mp.track(email, "New user signed up for marketing" , {} )
            mp.people_set(email, {"$created": str(timezone.now), "environment": ENVIRONMENT,})
            messages.add_message(request, messages.INFO, "Signed up for waiting list")
            welcome_new_marketing_lead(email)
            return render(request, "confirm_waitinglist.html")
        else:
            messages.add_message(request, messages.INFO, "Please provide a valid email address")
            return redirect("/")
    else:
        mp.track("unknown user", "Homepage",{"environment": ENVIRONMENT,})
        form = EmailMarketing()
    return render(request, "homepage.html", {"form":form})

def sign_up_marketing_email(self, request):
    if request.method == "POST":
        form = EmailMarketing(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            new_marketing_lead = EmailList(
                email = email,
            )
            new_marketing_lead.save()
            mp.track(email, "New user signed up for marketing" , {"environment": ENVIRONMENT,} )
            mp.people_set(email, {"$created": self.date_created, "environment": ENVIRONMENT,})
            welcome_new_marketing_lead(email)
            return render(request, "confirm_waitinglist.html")
        else:
            messages.add_message(request, messages.INFO, "Please provide a valid email address")
            return redirect("/")
    else:
        form = EmailMarketing()
        return render(request, "sign_up_marketing.html", {"form":form})


def legal_terms(request):
    mp.track("unknown user", "termsandconditions",{"environment": ENVIRONMENT,})
    return render(request, "terms.html", {})

def legal_privacy(request):
    mp.track("unknown user", "privacypolicy",{"environment": ENVIRONMENT,})
    return render(request, "privacy.html", {})

def product_cards(request):
    mp.track("unknown user", "productcards",{"environment": ENVIRONMENT,})
    return render(request, "productcards.html", {})

def product_platform(request):
    mp.track("unknown user", "productplatform",{"environment": ENVIRONMENT,})
    return render(request, "productplatform.html", {})

def product_workshop(request):
    mp.track("unknown user", "productworkshop",{"environment": ENVIRONMENT,})
    return render(request, "productworkshop.html", {})

def blog(request):
    mp.track("unknown user", "blog",{"environment": ENVIRONMENT,})
    return render(request, "blog.html", {})

def contact(request):
    if request.method == "POST":
        form = Orderform(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            description = form.cleaned_data["description"]
            new_order = Order(
                email = email,
                description = description,
            )
            new_order.save()
            mp.track(email, "New order received" , {"environment": ENVIRONMENT,} )
            mp.people_set(email, {"$created": str(timezone.now)})
            confirm_new_order(email)
            return render(request, "confirm_contact.html")
        else:
            messages.add_message(request, messages.INFO, "Please provide a valid email address")
            return redirect("/")
    else:
        mp.track("unknown user", "order page",{"environment": ENVIRONMENT,})
        form = Orderform()
        return render(request, "request_order.html", {"form":form})
