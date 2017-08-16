#coding=utf-8
from django import forms
from django.conf import settings
from users.models import User
from django.shortcuts import render,render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.hashers import make_password, check_password
from itsdangerous import URLSafeTimedSerializer, BadTimeSignature, SignatureExpired
from utils.utils import encode_URLSafeTimedToken, decode_URLSafeTimedToken
from django.core.mail import send_mail
from django.template import loader

from urllib import parse

# Create your views here.
active_salt = "active"
active_max_age = 86400

cookie_salt = "cookie"
cookie_max_age = 3600


class SignUpForm(forms.Form):
    username = forms.CharField(label='username:', max_length=50)
    password = forms.CharField(label='password:', widget=forms.PasswordInput())
    email = forms.EmailField(label='email:')


class SignInForm(forms.Form):
    username = forms.CharField(label='username:', max_length=50)
    password = forms.CharField(label='password:', widget=forms.PasswordInput())


def gen_cookie_token(cookie_message):
    s = URLSafeTimedSerializer(settings.SECRET_KEY)
    encoded = s.dumps(cookie_message, salt=cookie_salt)
    return encoded


def parse_message_from_cookie_token(cookie_token):
    s = URLSafeTimedSerializer(settings.SECRET_KEY)
    cookie_message = s.loads(cookie_token, max_age=cookie_max_age, salt=cookie_salt)
    return cookie_message


def gen_active_token(active_message):
    s = URLSafeTimedSerializer(settings.SECRET_KEY)
    encoded = s.dumps(active_message, salt=active_salt)
    return encoded


def parse_message_from_active_token(active_token):
    s = URLSafeTimedSerializer(settings.SECRET_KEY)
    active_message = s.loads(active_token, max_age=active_max_age, salt=active_salt)
    return active_message


def send_email_for_active(username, to_email):
    token = gen_active_token({"username": username, "email": to_email})
    context = {}
    context['username'] = username
    context['email'] = to_email
    context['link'] = "%s?%s" % (parse.urljoin(settings.SERVER, "users/active"), parse.urlencode({"token": token}))
    content = loader.render_to_string("active.email", context)
    code = send_mail(r"啾啾川用户激活邮件", content, settings.DEFAULT_FROM_EMAIL, [to_email])
    return code


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if not form.is_valid():
            return render(request, 'signup.html', {'form': form})
        else:
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            users = User.objects.filter(username=username, active=True)
            if len(users) != 0:
                return HttpResponse('用户名 %s 已经被注册' % username)
            users = User.objects.filter(email=email, active=True)
            if len(users) != 0:
                return HttpResponse('邮箱 %s 已经被注册' % email)

            encoded_password = make_password(password=password)
            user = User(username=username, password=encoded_password, email=email)
            user.save()
            send_email_for_active(username, email)
            return HttpResponse('check your email %s to active your account in 24h !!' % email)
    else:
        form = SignUpForm()
    return render(request, "signup.html", {'form': form})


def active_user(request):
    if request.method == 'GET':
        active_token = request.GET.get("token")
        try:
         message = parse_message_from_active_token(active_token)
        except BadTimeSignature as bt:
            return HttpResponse('激活时间已超时')
        except Exception as ex:
            return None

        username = message['username']
        email = message['email']
        users = User.objects.filter(username=username, active=True)
        if len(users) != 0:
            return HttpResponse('用户名 %? 已经被注册' % username)
        users = User.objects.filter(email=email, active=True)
        if len(users) != 0:
            return HttpResponse('邮箱 %? 已经被注册' % email)
        users = User.objects.filter(username=username, email=email)
        if len(users) == 0:
            return HttpResponse('没有关于账户 %s 和邮箱 %s 的任何注册信息' % (username, email))
        elif users[0].active:
            return HttpResponse('账户 %s 和邮箱 %s 已经被激活' % (username, email))
        elif not users[0].active:
            users[0].active = True
            users[0].save()
        return HttpResponse('激活成功')

def signin(request):
    if request.method == 'POST':
        form = SignInForm(request.POST)
        if not form.is_valid():
            return render(request, 'signin.html', {'form': form})
        else:
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            users = User.objects.filter(username=username)
            if len(users) == 0:
                return HttpResponse('账户 %s 不存在' % username)
            user = users[0]
            password_in_db = user.password
            if check_password(password, password_in_db):
                response = HttpResponseRedirect('/index/%s' % username)
                response.set_cookie('token', gen_cookie_token(username), 3000)
                return response
            else:
                return HttpResponseRedirect('/users/signin')
    else:
        form = SignInForm()

    return render(request,  'signin.html', {"form": form})
