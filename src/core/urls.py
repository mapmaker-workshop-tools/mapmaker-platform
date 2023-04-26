"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from django.contrib import admin

admin.site.site_header = 'Mapmaker.nl'                    # default: "Django Administration"
admin.site.index_title = 'Databases'                 # default: "Site administration"
admin.site.site_title = 'Makmaker Admin' # default: "Django site admin"


urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboard/', include('dashboard.urls')),
    path('workshop/', include('workshop.urls')),
    path('', include('homepage.urls')),
    path('/', include('homepage.urls')), 
    path('auth/', include('users.urls')),    
    path('user/', include('users.urls')),   
    path('accounts/', include('users.urls')),    
    path('card/', include('card_interactions.urls')),  
    path("__reload__/", include("django_browser_reload.urls")),
    path('api/', include('api.urls')),
]
