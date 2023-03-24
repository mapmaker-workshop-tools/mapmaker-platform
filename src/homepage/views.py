from django.shortcuts import render
from core.utils import mp

# Create your views here.
def index(request):
    mp.track('unknown user', 'Homepage',{'session': request.COOKIES['sessionid'],
    'HTTP_USER_AGENT': request.META['HTTP_USER_AGENT'],})
    return render(request, 'homepage.html')
