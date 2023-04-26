import ast

from card_interactions.models import Comment, Follower, Resource
from core.utils import mp, qrgenerator, signer
from django.contrib.auth.decorators import login_required
from django.db.models import Case, When
from django.shortcuts import HttpResponse, render
from emailhandler.standard_emails import workshop_summary
from users.models import CustomUser

from workshop.models import Card, Workshop


# Create your views here.
@login_required
def workshop_settings(request):
    current_user = request.user
    current_workshop = current_user.active_workshop
    cards = Card.objects.filter(workshop=current_workshop)
    Card.objects.filter(workshop=current_workshop).count()
    likecount = Follower.objects.filter(card_liked__workshop=current_workshop).count()
    commentcount = Comment.objects.filter(card__workshop=current_workshop).count()
    resourcecount = Resource.objects.filter(card__workshop=current_workshop).count()
    participants = Workshop.participants.through.objects.filter(workshop=current_workshop)
    participants.count()
    workshop_secret = signer.sign_object({"workshopid":current_workshop.id})
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
    qrcode = qrgenerator("https://mapmaker.nl/user/register/"+workshop_secret, workshop_secret)

    context = {
            "firstname": current_user.first_name,
            "cards": ordered_cards,
            "participants": participants,
            "workshop": current_workshop,
            "cardscount": cards.count() -200,
            "participantcount": participants.count(),
            "likecount":likecount,
            "commentcount":commentcount,
            "resourcecount":resourcecount,
            "workshop_secret":workshop_secret,
            "qrcode":qrcode,
            }
    mp.track(request.user.email, "Workshop settings", {
            "workshop": current_workshop.workshop_name,

            "HTTP_USER_AGENT": request.META["HTTP_USER_AGENT"],
            })
    return render(request, "workshop_settings.html", context)



def share_workshop(request, workshop_secret):
    workshopid_unsigned = int(signer.unsign_object(workshop_secret)["workshopid"])
    current_workshop = Workshop.objects.get(id=workshopid_unsigned)
    qrcode = qrgenerator("https://mapmaker.nl/user/register/"+workshop_secret, workshop_secret)
    context = {"workshop":current_workshop, "workshop_secret":workshop_secret, "qrcode":qrcode}
    return render(request, "workshop_share.html", context)

@login_required
def trigger_summary_email(request):
    current_user = request.user
    current_workshop = current_user.active_workshop
    id = current_workshop.id
    workshop_summary(id)
    mp.track(request.user.email, "Workshop summary sent ", {
            "workshop": current_workshop.workshop_name,
            "HTTP_USER_AGENT": request.META["HTTP_USER_AGENT"],
            })
    print("sending email to participants")
    return HttpResponse(status="204")
