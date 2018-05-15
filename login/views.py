# -*- coding: utf-8 -*-

# Python builtins
from __future__ import unicode_literals
import datetime
import random
import string
import os


# Custom Imports
from forms import UploadFileForm
from models import AppUser
from models import Document
import mail


from django.shortcuts import render
from forms import RegistrationForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
# from django.core.mail import send_mail
from threading import Thread
from django.core.files.storage import default_storage
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site


# Create your views here.

def register_user(request):
    user_exist = False
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            name = request.POST['username']
            current_site = get_current_site(request)
            print current_site
            try:
                user_exist = User.objects.get(username=name)
                print "USER EXIST ---------", user_exist
            except ObjectDoesNotExist:
                password = request.POST['password1']
                user = User.objects.create_user(name, name, password, is_active=False)
                key = ''.join(random.choice(string.digits + string.letters) for _ in range(10))
                app_user = AppUser(user=user, key_expires=timezone.now() + datetime.timedelta(minutes=3), activation_key=key)
                app_user.save()
                # activation_key = key, to = ['gopinath.r@jouve.com'])
                Thread(target=mail.registration_mail, kwargs={'host': current_site.domain, 'activation_key': key,
                                                              'to': ['gopinath.r@jouve.com']}).start()
                # mail.registration_mail(activation_key=key, to=['gopinath.r@jouve.com'])
                print 'mail sent success --------'
                return HttpResponseRedirect(reverse('login'))
    else:
        form = RegistrationForm()
    return render(request, 'login/register.html', {'form': form, 'user_exist': user_exist})


def verify_activation_key(request, key):
    app_user = AppUser.objects.get(activation_key=key)
    expire = app_user.key_expires < timezone.now()
    if not expire:
        app_user.user.is_active=True
        app_user.activated_on = timezone.now()
        print app_user.user.is_active
        app_user.user.save()
    return render(request, 'login/activate.html', {'app_user': app_user, 'key_expire': expire})


def resend_activation_key(request, key):
    app_user = AppUser.objects.get(activation_key=key)
    key = ''.join(random.choice(string.digits + string.letters) for _ in range(10))
    app_user.activation_key = key
    app_user.key_expires = timezone.now() + datetime.timedelta(minutes=3)
    app_user.save()
    mail.registration_mail(activation_key=key, to=['gopinath.r@jouve.com'])
    # return render(request,)

    # return HttpResponseRedirect(reverse('verify_activation_key', args=[key]))

# def handle_uploaded_file(f):
#     with open('name.txt', 'wb+') as destination:
#         for chunk in f.chunks():
#             destination.write(chunk)
def file_upload(request):
    save_path = os.path.join(settings.MEDIA_ROOT, 'uploads', 'test')
    print save_path
    path = default_storage.save(save_path, request.FILES['file'])
    print default_storage.path(path)
    return default_storage.path(path)

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # file_upload(request)  # This is for normal form upload(forms.form)
            form.save()
            # return HttpResponse('File uploaded sucessfully...')
            return render(request, 'login/view_upload.html', {'document': Document.objects.all(), 'current_date': timezone.now().date()})
    else:
        form = UploadFileForm()
    return render(request, 'login/upload.html', {'form': form})




