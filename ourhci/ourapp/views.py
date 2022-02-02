from django.shortcuts import render
from django.urls import reverse
from django.http import  HttpResponseRedirect

# Create your views here.
def index(request):

    return render(request, "ourapp/index.html")