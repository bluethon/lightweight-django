#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date     : 2017-07-16 15:30
# @Author   : Bluethon (j5088794@gmail.com)
# @Link     : http://github.com/bluethon

from django.conf.urls import url

from .views import page

urlpatterns = (
    url(r'^(?P<slug>[\w./-]+)/$', page, name='page'),
    url(r'^$', page, name='homepage'),
)
