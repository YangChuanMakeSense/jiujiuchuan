#coding=utf-8

from django.shortcuts import render
from django.http import HttpResponse
from django import forms
# Create your views here.


class BlogEditForm(forms.Form):
    title = forms.CharField(label='username:', max_length=100)
    tag = forms.


def blog_edit(request, username="No One"):
    if request.method == 'GET':
        return
    return HttpResponse(r'编辑博客: %s' % username)