from django.http import HttpResponse
from workshop.models import Card, Workshop


#Healthcheck for AWS. Helps us to validate the server is up 
def status(request):
    return HttpResponse("up.")


#This function helps us upload images
def import_images_as_cards(request, workshop_id):
    workshop = Workshop.objects.get(id=workshop_id)
    cards = Card.objects.filter(workshop=workshop, cardtype='empty')
    print(workshop)
    print(cards.count())
    return HttpResponse("test.") 