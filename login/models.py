# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from django.utils import timezone



class EmailBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        print 'IN AUTNTHENTICATE ###########################'
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=username)
        except UserModel.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
        return None

    # def get_user(self, user_id):
    #     try:
    #         print 'GET USER @@@@@@@@@@@@@@@@@@@@@@'
    #         return User.objects.get(pk=user_id)
    #     except User.DoesNotExist:
    #         return None


class AppUser(models.Model):
    user = models.OneToOneField(User)
    activation_key = models.CharField(max_length=100, unique=True)
    key_expires = models.DateTimeField()
    activated_on = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["user", "activated_on"]


    # def is_key_expire(self):
    #     if self.key_expires > timezone.now():
    #         return False
    #     return True

class Document(models.Model):
    audio = models.FilePathField(path='/home/dev/connectus/media/uploads/testupload', match='foo.*\.txt', recursive=True)
    upload_by = models.ForeignKey('auth.User', related_name='uploaded_documents')
    datestamp = models.DateTimeField(auto_now_add=True)
    document = models.FileField()