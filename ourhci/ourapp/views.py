from django.shortcuts import render
from django.urls import reverse
from django.http import  HttpResponseRedirect, Http404
from django.core.exceptions import PermissionDenied
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from .models import User, Post
from django.conf import settings
from django import forms
from django.forms import ModelForm, formset_factory, modelformset_factory
import pyperclip
import datetime
import markdown2
# Forms
class editprofileform(ModelForm):
    class Meta:
        model = User
        fields = ["email", "bio"]


# Create your views here.
def error_404(request, exception):
        data = {}
        return render(request,'ourapp/404.html', data)



def index(request):
    user = request.user
    developer = user.groups.filter(name='Developer').exists()
    feed = Post.objects.all()

    return render(request, "ourapp/index.html", {
        "developer": developer,
        "feed":feed
    })




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
            c_indic = hciclass[1].lower()
            if c_indic == "i":
                user.consortium = "iSpark"
            elif c_indic == "a":
                user.consortium = "Aphelion"
            elif c_indic == "o":
                user.consortium = "Ortus"
            elif c_indic == "p":
                user.consortium = "ProEd"
                    
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
        try:
            user_data = User.objects.get(username=username)
        except:
            raise Http404

        return render(request, "ourapp/profile.html",{
            "data":user_data
        })

def user_search(request):
    if request.method == "POST":
        pass
    else:
        return render(request, "ourapp/users.html")

def search(request):
    query = str(request.GET.get('q', 1))
    searchq = query.upper()
    searchq.strip()
    searchq = searchq.replace(' ', '')

    
    try:
        h = User.objects.get(username=searchq)
        return HttpResponseRedirect(reverse("profile", kwargs={"username":searchq}))
    except:
        data = User.objects.all()
        list = []
        for user in data:
            if searchq in user.username:
                list.append(user)
        return render(request, "ourapp/user_search_results.html", {
            "data": list,
            "searchq" : query
        })

def profile_edit(request, username):
    if request.user.username != username:
        raise PermissionDenied()
    if request.method == "POST":
        form = editprofileform(request.POST)
        if form.is_valid():

            new_email = form.cleaned_data["email"]
            new_bio =  form.cleaned_data["bio"]
            editor = User.objects.get(username=username)
            editor.bio = new_bio
            editor.email = new_email
            editor.save()
            return HttpResponseRedirect(reverse("profile", kwargs={"username":username}))
        else:
            return HttpResponseRedirect(reverse("editprofile",  kwargs={"username":username}))    
    else:
        userdata = User.objects.get(username=username)
        return render(request, "ourapp/edit_profile.html", {
            "user":userdata,
            "form":editprofileform
        })