from django.core.mail import EmailMessage
from django.core import mail
from django.db.models import Count, Q
from workshop.models import Card, Workshop
from users.models import CustomUser as User
from card_interactions.models import Follower, Comment, Resource
connection = mail.get_connection()


def send_simple_email(recipient):
    print('Sending simple email')
    sender = 'mapmaker.server@gmail.com'
    bcc_recipients = [recipient]
    email = EmailMessage(
        'Hello',
        'Body goes here',
        sender,
        bcc_recipients,
        reply_to=[sender],
        headers={'Message-ID': 'foo'},
    )
    email.send()

    
def welcome_new_marketing_lead(recipient):
    sender = 'mapmaker.server@gmail.com'
    bcc_recipients = [recipient]
    email = EmailMessage(
        'Thanks for joining the Mapmaker email list',
        'Thanks for joining the Mapmaker email list, we will let you know once we launch!',
        sender,
        bcc_recipients,
        reply_to=[sender],
    )
    email.send()
    
    
def welcome_new_user(recipient, workshop_name):
    sender = 'mapmaker.server@gmail.com'
    bcc_recipients = [recipient]
    email = EmailMessage(
        'Here is your mapmaker account for '+workshop_name,
        'Your account with Mapmaker was created succesfully. Now you can view and edit '+workshop_name+'\n\nLog in to https://mapmaker.nl.',
        sender,
        bcc_recipients,
        reply_to=[sender],
    )
    email.send()

def notify_followers_new_post(cardid):
    card = Card.objects.get(id=cardid)
    followers = Follower.objects.filter(card_liked=card)
    last_comments = Comment.objects.filter(card=card).order_by('-id')[:5]
    last_comments= reversed(last_comments)
    subject = "New update in Mapmaker on card: " + card.title
    message = "A new update was posted on a card you follow \nHere are the last updates in the discussion:\n\n"
    for comment in last_comments:
        message += comment.author.first_name +' from ' + comment.author.organisation + " said: " + comment.comment_text + "\n"
    message += "\n\nLog in to mapmaker.nl to join the discussion"
    connection.open()
    messageque = []
    for follower in followers:
        email = mail.EmailMessage(
            subject,
            message,
            'mapmaker.server@gmail.com',
            [follower.user_like.email],
            connection=connection,
        )
        messageque.append(email)
    connection.send_messages(messageque)
    connection.close()


def workshop_summary(workshopid):
    workshop = Workshop.objects.get(id=workshopid)
    subject = "Throwback of your Mapmaker workshop: " + workshop.workshop_name
    message = "Hi!,\n\nYou were part of a workshop with Mapmaker.nl. We hoped you really liked it! \nTo ensure you get the most out of the session we uploaded the session with all of the cards you created to your own personalised dashboard. This should enable you to keep in touch with your peers and send updates on the progress you made.\n\nlog in to mapmaker.nl to see all details, here is the recap of your session:\n\n"
    #Getting some statistics
    workshop_owner = workshop.workshop_owner
    message += 'The workshop was organised by ' + workshop_owner.first_name + " "+workshop_owner.last_name + " who works at " + workshop_owner.organisation
    participants = Workshop.participants.through.objects.filter(workshop=workshop)
    participantcount = str(participants.count())
    message += ' who managed to invite ' + participantcount+ " to the workshop!\n"

    resourcecount = str(Resource.objects.filter(card__workshop=workshop).count())
    message += '\nTogether you shared ' + resourcecount+ " resources related to subjects you discussed. \n"
    commentcount = str(Comment.objects.filter(card__workshop=workshop).count())
    message += 'You collaborated by writing ' + commentcount+ " comments on all cards combined. \n"
    likecount = str(Follower.objects.filter(card_liked__workshop=workshop).count())
    message += 'You stayed up to date and followed ' + commentcount+ " cards between all participants. \n"
    cardcount = str(Card.objects.filter(workshop=workshop).filter(~Q(cardtype='empty')).count())
    message += '\nIn total you created ' + cardcount+ " cards full of ideas and concerns. The most popular ones are\n"
    populaircard_bycomment = Card.objects.alias(num_comments=Count('commented_card')).order_by('-commented_card')[:3]
    populaircard_bylikes = Follower.objects.values("card_liked").annotate(count=Count('card_liked')).order_by("-count")[:3]
    populairuser_byresource = Resource.objects.values("owner").annotate(count=Count('owner')).order_by("-count")[:3]
    populairuser_bycomment = Comment.objects.values("author").annotate(count=Count('author')).order_by("-count")[:3]
    message += 'These cards were discussed most: \n'
    for card in populaircard_bycomment:
        message += card.cardtype + " " + card.title +' from ' + card.author.first_name + "\n"
    
    message += '\n\nThese are the cards with the most followers: \n'
    for card in populaircard_bylikes:
        fetch_card = Card.objects.get(id=card['card_liked'])
        number_of_likes = str(card['count'])
        message += number_of_likes +" Followers for: " + fetch_card.title +' from ' + fetch_card.author.first_name + "\n"   
        
    message += '\n\nSome of you went all out during the workshop, here are some of the most active users during the workshop: \n'
    for user in populairuser_byresource:
        fetch_user = User.objects.get(id=user['owner'])
        number_of_resources = str(user['count'])
        message += fetch_user.first_name +' from ' + fetch_user.organisation + " shared "+ number_of_resources +" resources!"+ "\n" 
    for user in populairuser_bycomment:
        fetch_user = User.objects.get(id=user['author'])
        number_of_comments = str(user['count'])
        message += fetch_user.first_name +' from ' + fetch_card.author.organisation + " wrote "+ number_of_comments +" updates!"+ "\n" 
    message += '\n\nTo see all details log in to mapmaker.nl. \n'
    userIDlist =[]
    for i in participants:
        userIDlist.append(i.customuser_id)
    #Get all the participants to this session --> This ensures we can query their details in templates
    participants = User.objects.filter(pk__in=userIDlist)
    
    connection.open()
    messageque = []
    for participant in participants:
        email = mail.EmailMessage(
            subject,
            message,
            'mapmaker.server@gmail.com',
            [participant.email],
            connection=connection,
        )
        messageque.append(email)
    connection.send_messages(messageque)
    connection.close()
    


