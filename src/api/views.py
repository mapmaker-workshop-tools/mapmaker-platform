from django.http import HttpResponse
from workshop.models import Card, Workshop
from users.models import CustomUser
from django.views.decorators.csrf import csrf_exempt
import ast


#Healthcheck for AWS. Helps us to validate the server is up 
def status(request):
    return HttpResponse("up.")


#This function helps us upload images
@csrf_exempt
def import_images_as_cards(request, workshop_id):
    workshop = Workshop.objects.get(id=workshop_id)
    author = CustomUser.objects.get(email='peter@petervandoorn.com')
    cards = Card.objects.filter(workshop=workshop, cardtype='empty')
    new_card = cards.latest('pk')
    new_card.cardtype = "image_card"
    new_card.author = author
    new_card.workshop = workshop
    new_card.title = 'Automatically imported by Mapmaker',
    new_card.description='This card was automatically imported by Mapmaker after your workshop. Claim it by making a edit',
    new_card.image = request.FILES["file"]
    new_card.save()
    return HttpResponse("Server Received a new image - Creating Card") 