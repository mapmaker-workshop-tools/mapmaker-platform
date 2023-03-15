from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import CustomUserLoginForm, CustomUserProfile
from users.models import CustomUser


# Create your views here.
def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.add_message(request, messages.INFO, 'welcome back ' + user.first_name)
            return redirect('/dashboard')
        else:
            messages.add_message(request, messages.INFO, 'Invalid username or password')
            return redirect('/user/login')
    else:
        form = CustomUserLoginForm()
        return render(request, 'login.html', {'form':form})
    
def logout_view(request):
    logout(request)
    messages.add_message(request, messages.INFO, 'Logged out')
    return redirect('/')

def register(request):
    return render(request, 'register.html')

def profile(request):
    current_user = request.user
    form = CustomUserLoginForm()
    return render(request, 'userprofile.html', {'user': current_user, 'form':CustomUserProfile})

def profile_edit(request, id):
    if request.user.id == id:    
        if request.method == 'POST':
            firstname = request.POST['firstName']
            lastname = request.POST['lastname']
            email = request.POST['email']
            organisation = request.POST['organisation']
            linkedin = request.POST['linkedin']
            messages.add_message(request, messages.INFO, 'Updated profile')
            print(request.user)
            return render(request, 'user_profile_table.html')

        elif request.method == 'GET':
            return render(request, 'user_profile_table_edit.html')
    else: 
        return HttpResponse(status=403)