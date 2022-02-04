from django.shortcuts import render
from django.urls import reverse
from django.http import  HttpResponseRedirect, Http404
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from .models import User
from django.conf import settings
from django import forms
from django.forms import ModelForm

# Create your views here.
def error_404(request, exception):
        data = {}
        return render(request,'ourapp/404.html', data)



def index(request):
    user = request.user
    developer = user.groups.filter(name='Developer').exists()
    return render(request, "ourapp/index.html", {
        "developer": developer
    })


def about(request):
    return render(request, "ourapp/about.html")

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "ourapp/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "ourapp/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        hciclass = request.POST['class']
        if password != confirmation:
            return render(request, "ourapp/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.hciclass = hciclass
            user.save()
        except IntegrityError:
            return render(request, "ourapp/register.html", {
                "message": "You have already registered! Please contact staff if this is a mistake."
            })
        

        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "ourapp/register.html")

def profile(request, username):
    if request.method == "POST":
        pass
    else:
        if username == "ourhcitest+admin":
            raise Http404
        user_data = User.objects.get(username=username)
        return render(request, "ourapp/profile.html",{
            "data":user_data
        })