#coding=utf-8
from django.db import models
from django.contrib.auth.hashers import make_password, check_password

# Create your models here.
# user (username, password, email, view_count, signature)


class User(models.Model):
    username = models.CharField(max_length=50, primary_key=True)
    email = models.EmailField(unique=True, db_index=True)
    password = models.CharField(max_length=50)
    view_count = models.IntegerField(db_index=True, default=0)
    signature = models.CharField(max_length=50, default="")
    active = models.BooleanField(default=False)

