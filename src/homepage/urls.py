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
from homepage import views
from django.urls import path



urlpatterns = [
    path('', views.index, name='homepage'),
    path('legal/terms', views.legal_terms, name='homepage'),
    path('legal/privacy', views.legal_privacy, name='homepage'),
    path('product/cards', views.product_cards, name='homepage'),
    path('product/platform', views.product_platform, name='homepage'),
    path('product/workshop', views.product_workshop, name='homepage'),
    path('emaillist', views.sign_up_marketing_email, name='sign up for marketing'),
    path('blog', views.blog, name='Blog'),
    path('contact', views.contact, name='contact')
]
