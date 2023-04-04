from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string, get_template
from django.template import Context

from django.core import mail
from django.db.models import Count, Q
from workshop.models import Card, Workshop
from users.models import CustomUser as User
from card_interactions.models import Follower, Comment, Resource
connection = mail.get_connection()


def standard_email(username, subject, recipient, CTA_TEXT, CTA_URL, TOP_TEXT, BOTTOM_TEXT ):
    plaintext = get_template('email_base.txt')
    htmly     = get_template('email_base.html')

    context = {'username': username, 'CTA_TEXT': CTA_TEXT, 'CTA_URL':CTA_URL, 'TOP_TEXT':TOP_TEXT, "BOTTOM_TEXT": BOTTOM_TEXT}

    subject, from_email, to = subject, 'mapmaker.server@gmail.com', recipient
    text_content = plaintext.render(context)
    html_content = htmly.render(context)
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


    
def welcome_new_marketing_lead(recipient):
    standard_email(recipient, 
                'Thanks for joining the Mapmaker email list', 
                recipient,
                'Read our blog',
                'https://mapmaker.nl/blog',
                'Welcome to Mapmaker! Thanks for joining the Mapmaker email list, we will let you know once we launch! In the meantime:',
                'If you have any questions, or want to get in touch feel free to send a message: https://mapmaker.nl/contact'
                )
    
    
def confirm_new_order(recipient):
    standard_email(recipient, 
                'We received your request', 
                recipient,
                'Read our blog',
                'https://mapmaker.nl/blog',
                'Thanks for your message! We love questions. We will get back to you asap, usually within 24H. In the meantime:',
                'If you have any questions, or want to get in touch feel free to send a message: https://mapmaker.nl/contact'
                )
    
    
    
    sender = 'mapmaker.server@gmail.com'
    bcc_recipients = ['peter@petervandoorn.com']
    email = EmailMessage(
        'A new message was send through the mapmaker website',
        'Check it out: https://mapmaker.nl/admin',
        sender,
        bcc_recipients,
        reply_to=[sender],
    )
    email.send()
    
    
def welcome_new_user(recipient, workshop_name):
    standard_email(recipient, 
                'Here is your mapmaker account for'+workshop_name, 
                recipient,
                'Log in to: '+workshop_name,
                'https://mapmaker.nl/user/login',
                'Your account with Mapmaker was created succesfully. You can now view and edit',
                'If you want to learn more about what Mapmaker is, check out our blog: https://mapmaker.nl/blog'
                )

def notify_followers_new_post(cardid):
    card = Card.objects.get(id=cardid)
    followers = Follower.objects.filter(card_liked=card)
    last_comments = Comment.objects.filter(card=card).order_by('-id')[:5]
    last_comments= reversed(last_comments)
    subject = "New update in Mapmaker on card: " + card.title
    message = "A new update was posted on a card you follow \nHere are the last updates in the discussion:\n\n"
    for comment in last_comments:
        message += comment.author.first_name +' from ' + comment.author.organisation + " said: " + comment.comment_text + "\n"
    for follower in followers:
        standard_email(follower.user_like.first_name, 
                "New update in Mapmaker on card: " + card.title, 
                follower.user_like.email,
                'View ' +card.title,
                'https://mapmaker.nl/dashboard',
                message,
                'Log in to mapmaker.nl to join the discussion, if you forgot your password simply reset it here: https://mapmaker.nl/user/reset_password/'
                )        



def workshop_summary(workshopid):
    workshop = Workshop.objects.get(id=workshopid)
    subject = "Throwback of your Mapmaker workshop: " + workshop.workshop_name
    message = "You were part of a workshop with Mapmaker.nl. We hoped you really liked it! \nTo ensure you get the most out of the session we uploaded the session with all of the cards you created to your own personalised dashboard. This should enable you to keep in touch with your peers and send updates on the progress you made.\n\n"
    #Getting some statistics
    workshop_owner = workshop.workshop_owner
    message += 'The workshop was organised by ' + workshop_owner.first_name + " "+workshop_owner.last_name + " who works at " + workshop_owner.organisation
    participants = Workshop.participants.through.objects.filter(workshop=workshop)
    participantcount = str(participants.count())
    message += ' who managed to invite ' + participantcount+ " people to the workshop!\n"

    resourcecount = str(Resource.objects.filter(card__workshop=workshop).count())
    message += '\nTogether you shared ' + resourcecount+ " resources related to subjects you discussed. \n"
    commentcount = str(Comment.objects.filter(card__workshop=workshop).count())
    message += 'You collaborated by writing ' + commentcount+ " comments on all cards combined. \n"
    likecount = str(Follower.objects.filter(card_liked__workshop=workshop).count())
    message += 'You stayed up to date and followed ' + commentcount+ " cards between all participants. \n"
    cardcount = str(Card.objects.filter(workshop=workshop).filter(~Q(cardtype='empty')).count())
    message += '\nIn total you created ' + cardcount+ " cards full of ideas and concerns. These cards were discussed the most:\n"
    populaircard_bycomment = Card.objects.alias(num_comments=Count('commented_card')).order_by('-commented_card')[:3]
    populaircard_bylikes = Follower.objects.values("card_liked").annotate(count=Count('card_liked')).order_by("-count")[:3]
    populairuser_byresource = Resource.objects.values("owner").annotate(count=Count('owner')).order_by("-count")[:3]
    populairuser_bycomment = Comment.objects.values("author").annotate(count=Count('author')).order_by("-count")[:3]
    for card in populaircard_bycomment:
        message += "-- "+card.cardtype + " " + card.title +' from ' + card.author.first_name + "\n"
    
    message += '\n\nThese are the cards with the most followers: \n'
    for card in populaircard_bylikes:
        fetch_card = Card.objects.get(id=card['card_liked'])
        number_of_likes = str(card['count'])
        message += "-- "+ number_of_likes +" Followers for: " + fetch_card.title +' from ' + fetch_card.author.first_name + "\n"   
        
    message += '\n\nSome of you went all out during the workshop, here are some of the most active users during the workshop: \n'
    for user in populairuser_byresource:
        fetch_user = User.objects.get(id=user['owner'])
        number_of_resources = str(user['count'])
        message += "-- "+fetch_user.first_name +' from ' + fetch_user.organisation + " shared "+ number_of_resources +" resources!"+ "\n" 
    
    message += '-------------------------\n'
    for user in populairuser_bycomment:
        fetch_user = User.objects.get(id=user['author'])
        number_of_comments = str(user['count'])
        message += "-- "+fetch_user.first_name +' from ' + fetch_card.author.organisation + " wrote "+ number_of_comments +" updates!"+ "\n" 
    userIDlist =[]
    for i in participants:
        userIDlist.append(i.customuser_id)
    #Get all the participants to this session --> This ensures we can query their details in templates
    participants = User.objects.filter(pk__in=userIDlist)
    
    connection.open()
    messageque = []
    for participant in participants:
        standard_email(participant.first_name, 
                subject, 
                participant.email,
                'Log in to go back to workshop: ' +workshop.workshop_name,
                'https://mapmaker.nl/dashboard',
                message,
                'Log in to mapmaker.nl to join the discussion, if you forgot your password simply reset it here: https://mapmaker.nl/user/reset_password/'
                )
    


