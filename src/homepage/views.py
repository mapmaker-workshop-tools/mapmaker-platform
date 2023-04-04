from django.shortcuts import render, redirect
from core.utils import mp
from django.utils import timezone
from .forms import EmailMarketing
from .models import EmailList
from django.contrib import messages
from emailhandler.standard_emails import welcome_new_marketing_lead

# Create your views here.
def index(request):
    if request.method == "POST":
        form = EmailMarketing(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            new_marketing_lead = EmailList(
                email = email,
            )
            new_marketing_lead.save()
            mp.track(email, 'New user signed up for marketing' , {'HTTP_USER_AGENT': request.META['HTTP_USER_AGENT'],} )
            mp.people_set(email, {'$created': str(timezone.now)})
            messages.add_message(request, messages.INFO, 'Signed up for waiting list')
            welcome_new_marketing_lead(email)
            return redirect('/')
        else:
            messages.add_message(request, messages.INFO, 'Please provide a valid email address')
            return redirect('/')
    else:
        mp.track('unknown user', 'Homepage',{'HTTP_USER_AGENT': request.META['HTTP_USER_AGENT'],})
        form = EmailMarketing()
    return render(request, 'homepage.html', {'form':form})

def sign_up_marketing_email(request):
    if request.method == "POST":
        form = EmailMarketing(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            new_marketing_lead = EmailList(
                email = email,
            )
            new_marketing_lead.save()
            mp.track(email, 'New user signed up for marketing' , {'HTTP_USER_AGENT': request.META['HTTP_USER_AGENT'],} )
            mp.people_set(email, {'$created'       : self.date_created,})
            welcome_new_marketing_lead(email)
            messages.add_message(request, messages.INFO, 'Signed up for waiting list')
            return redirect('/')
        else:
            messages.add_message(request, messages.INFO, 'Please provide a valid email address')
            return redirect('/')
    else:
        form = EmailMarketing()
        return render(request, 'sign_up_marketing.html', {'form':form})
    
    
def legal_terms(request):
    mp.track('unknown user', 'termsandconditions',{'HTTP_USER_AGENT': request.META['HTTP_USER_AGENT'],})
    return render(request, 'terms.html', {})

def legal_privacy(request):
    mp.track('unknown user', 'privacypolicy',{'HTTP_USER_AGENT': request.META['HTTP_USER_AGENT'],})
    return render(request, 'privacy.html', {})

def product_cards(request):
    mp.track('unknown user', 'productcards',{'HTTP_USER_AGENT': request.META['HTTP_USER_AGENT'],})
    return render(request, 'productcards.html', {})

def product_platform(request):
    mp.track('unknown user', 'productplatform',{'HTTP_USER_AGENT': request.META['HTTP_USER_AGENT'],})
    return render(request, 'productplatform.html', {})

def product_workshop(request):
    mp.track('unknown user', 'productworkshop',{'HTTP_USER_AGENT': request.META['HTTP_USER_AGENT'],})
    return render(request, 'productworkshop.html', {})