"""SmartParking URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
from smart_parking.views import *
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^dashboard/$', dashboard, name='index'),
    url(r'^input/',bookyourslot, name='book'),
    url(r'^accounts/profile/',home, name='home'),
    #url(r'^input-html/', input_html, name='input-html'),
    #url(r'^find/', find, name='find'),
    #url(r'^input$', input, name='login'),
    #url(r'^users/login/$', auth.login, {'template_name': 'login.html'}, name='login'),
    url(r'^login/$', auth.login, {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$',auth.logout, name='logout'),
    #url(r'^find-park/', find_parking, name='find-park'),
    url(r'^$',home, name='home'),
    url(r'^cancel/',cancelyourslot, name='cancel'),
    url(r'^all_slots/',all_slots, name='all_slots'),
    url(r'^book_slot/',book_slot, name='book_slot'),
    url(r'^show/',show, name='show'),

] +static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

#urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
