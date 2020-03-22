from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    return HttpResponse("Hello World, You are at genres index.")

def detail(request, id):
    return HttpResponse("Hello World, You are at genre {id}.".format(id=id))
