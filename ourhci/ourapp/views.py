from django.shortcuts import render
from django.urls import reverse
from django.http import  HttpResponseRedirect, Http404, HttpResponse, JsonResponse
from django.core.exceptions import PermissionDenied
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from .models import User, Post, UserFollow
from django.conf import settings
from django import forms
from django.forms import ModelForm, formset_factory, modelformset_factory
import pyperclip
import datetime
import markdown2
from markdownify import markdownify as md
from django.contrib.auth.decorators import login_required

bannedwords = ["shit", "fuck", "dick", "nigger", "penis", "what happened at tiananmen square", "clumptyduff", "cunt"]
# Forms
class editprofileform(ModelForm):
    class Meta:
        model = User
        fields = ["email", "bio"]

class NewForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea)
    # image = forms.FileField(required=False)
    #image = idk


# Views
def error_404(request, exception):
    data = {}
    return render(request,'ourapp/404.html', data)


def rick(request):
    return render(request, 'ourapp/rick.html')

def index(request):
    user = request.user
    developer = user.groups.filter(name='Developer').exists()
    feed = Post.objects.all().order_by('-id')
    return render(request, "ourapp/index.html", {
        "developer": developer,
        "feed": feed,
    })

@login_required
def make_post(request):
    if request.method == "POST":
        user = request.user
        content = markdown2.markdown(request.POST['content'])
        for bannedword in bannedwords:
            if bannedword.upper() in content.upper():
                return render(request, "ourapp/youshallnotpass.html", {
                    "url": "new"
                })
        # image = request.POST["image"]
        creation = Post.objects.create(
            user = user,
            content = content,
            # image = image,
        )
        creation.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "ourapp/new.html", {
            'form' : NewForm,
        })

def error418(request):
    return render(request, 'ourapp/418.html')

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
        if request.user.is_authenticated:
            print("already logged in")
            return HttpResponseRedirect(reverse("error418"))
        return render(request, "ourapp/login.html")

def logout_view(request):
    if not request.user.is_authenticated:
        print("not logged in")
        return HttpResponseRedirect(reverse("error418"))
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
        try:
            c_indic = hciclass[1].lower()
        except: 
            return render(request, "ourapp/register.html", {
                "message": "Please enter a valid HCI class!."
            })        
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
            elif c_indic == "L":
                user.consortium = "Lbozo"          
            user.save()
        except IntegrityError:
            return render(request, "ourapp/register.html", {
                "message": "An account has already been registered under this name. Please login"
            })
        

        return HttpResponseRedirect(reverse("index"))
    else:
        if request.user.is_authenticated:
            print("already logged in")
            return HttpResponseRedirect(reverse("error418"))
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

    if request.user.is_authenticated == True:
        if len(UserFollow.objects.all().filter(follower = request.user, following = User.objects.all().get(username=username))) == 0:
            following = None
        elif request.user.username == username:
            following = None
        else:
            following = True
    else:
        following = None

    return render(request, "ourapp/profile.html",{
        "data": user_data,
        "following": following,
    })

def user_search(request):
    if request.method == "POST":
        pass
    else:
        return render(request, "ourapp/users.html")

def search(request):
    # make searchq equal query stripped and caps
    query = str(request.GET.get('q', 1))
    query.strip()
    searchq = query.replace(' ', '')

    # get search filter
    search_filter = str(request.GET.get('filter', 1))

    if search_filter == "filter_username":
        searchq = searchq.upper()
        try:
            h = User.objects.get(username=searchq)
            return HttpResponseRedirect(reverse("profile", kwargs={"username":searchq}))
        except:
            data = User.objects.all()
            user_list = []
            for user in data:
                if searchq in user.username:
                    user_list.append(user)
            return render(request, "ourapp/user_search_results.html", {
                "data": user_list,
                "searchq" : query
            })
    else:
        data = User.objects.filter(hciclass__contains=searchq)
        return render(request, "ourapp/user_search_results.html", {
            "data": data,
            "searchq": query
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
            "user": userdata,
            "form": editprofileform
        })

@login_required
def follow(request, username):
    if len(UserFollow.objects.all().filter(follower = request.user, following = User.objects.all().get(username=username))) == 0:
        UserFollow.objects.create(
            follower = request.user,
            following = User.objects.all().get(username=username)
        )
    else:
        pass
    return HttpResponseRedirect(reverse("profile",  kwargs={"username":username}))   

@login_required
def unfollow(request, username):
    follow_ties = UserFollow.objects.all().filter(follower = request.user, following = User.objects.all().get(username=username))
    if len(follow_ties) != 0:
        for follow in follow_ties:
            follow.delete()
    else:
        pass
    return HttpResponseRedirect(reverse("profile",  kwargs={"username":username})) 

def edit(request, post_id):
    if request.method == "GET":
        post = Post.objects.all().get(id=post_id)
        post_content = md(post.content,  heading_style="ATX")
        return render(request, "ourapp/edit.html", {
            'user': request.user,
            'post': post,
            'post_content': post_content
        })
    else:
        post = Post.objects.all().get(id=post_id)
        post.content = markdown2.markdown(request.POST['content'])
        for bannedword in bannedwords:
            if bannedword.upper() in post.content.upper():
                return render(request, "ourapp/youshallnotpass.html", {
                    "url": "edit/" + str(post_id)
                })
        post.save()

        return HttpResponseRedirect('/')

def delete(request, post_id):
    post = Post.objects.all().get(id=post_id)
    post.delete()
    return HttpResponseRedirect('/')