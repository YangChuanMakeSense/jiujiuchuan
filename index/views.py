#coding=utf-8

from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.



def index(request, username="No One"):
    return HttpResponse(r'这是你的主页: %s' % username)
