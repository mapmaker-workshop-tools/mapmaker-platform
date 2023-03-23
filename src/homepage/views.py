from django.shortcuts import render
from core.utils import mp

# Create your views here.
def index(request):
    mp.track('unknown user', 'Homepage')
    return render(request, 'homepage.html')
