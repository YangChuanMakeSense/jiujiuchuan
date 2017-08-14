#coding=utf-8
from django import forms
from users.models import User
from django.shortcuts import render,render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.hashers import make_password, check_password


# Create your views here.

class UserForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=50)
    password = forms.CharField(label='密码', widget=forms.PasswordInput())


def signup(request):
    if request.method == 'POST':
        uf = UserForm(request.POST)
        if uf.is_valid():
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']
            email = uf.changed_data['email']
            encoded_password = make_password(password=password)
            User.objects.create(username=username, password=encoded_password, email=email)
            return HttpResponse('signup success!!')
    else:
        uf = UserForm()
    return render_to_response('signup.html', {'uf': uf}, context_instance=RequestContext(request))

def signin(request):
    pass
