"""connectus URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

import django.contrib.auth.views
import login.views
import login.forms
import login

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^register/$', login.views.register_user, name='register'),
    url(r'^login/$', django.contrib.auth.views.login,
        {
            'template_name': 'login/login.html',
            'authentication_form': login.forms.LoginForm,
        },
        name='login'
        ),
    url(r'^connectus/account/activation/(?P<key>[a-zA-Z0-9-]+)', login.views.verify_activation_key, name='verify_activation_key'),
    url(r'^connectus/account/resend/activation/(?P<key>[a-zA-Z0-9-]+)', login.views.resend_activation_key,
        name='resend_activation_key'),
    url(r'^connectus/upload$', login.views.upload_file, name='upload_file')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

