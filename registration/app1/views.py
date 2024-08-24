from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.cache import never_cache

def base(request):
    return render(request,'base.html')

@login_required(login_url='login')
def home_page(request):
    return render(request, 'home.html')

@never_cache
def signup_page(request):
    if request.method == 'POST':
        usname = request.POST.get('username')
        usmail = request.POST.get('email')
        uspass = request.POST.get('password1')
        uspassconf = request.POST.get('password2')

        if uspass != uspassconf:
            messages.error(request, "Passwords do not match!")
        else:
            my_user = User.objects.create_user(usname, usmail, uspass)
            my_user.save()
            return redirect('login')

    return render(request, 'signup.html')

@never_cache
def login_page(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        ussname = request.POST.get('username')
        pass1 = request.POST.get('pass')
        user = authenticate(request, username=ussname, password=pass1)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid credentials!")

    return render(request, 'login.html')

def logout_page(request):
    logout(request)
    return redirect('login')
