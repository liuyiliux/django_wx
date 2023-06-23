"""django_wx URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path

from myapp.views import get_weatherinfo_base, get_weatherinfo_all, register, sendcode, login,wx_login, geturl, add_href, \
    delete_href,logintoken

urlpatterns = [
    re_path(r'^get_weatherinfo_base/(?P<city>.*)/$',get_weatherinfo_base.as_view(), name="api"),
    re_path(r'^get_weatherinfo_all/(?P<city>.*)/$',get_weatherinfo_all.as_view(), name="api"),
    re_path(r'^register/$', register.as_view(), name="api"),
    re_path(r'^sendcode/$', sendcode.as_view(), name="api"),
    re_path(r'^login/$', login.as_view(), name="api"),
    re_path(r'^wx_login/$', wx_login.as_view(), name="api"),
    re_path(r'^logintoken/$', logintoken.as_view(), name="api"),
    re_path(r'^geturl/$', geturl.as_view(), name="api"), #获取超链接
    re_path(r'^add_href/$', add_href.as_view(), name="api"),#增加超链接
    re_path(r'^delete_href/$', delete_href.as_view(), name="api"),#删除超链接


]
