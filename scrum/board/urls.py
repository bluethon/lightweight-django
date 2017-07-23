#!/usr/bin/env python3
# encoding: utf-8
# @Date     : 2017-07-24 00:00
# @Author   : Bluethon (j5088794@gmail.com)
# @Link     : http://github.com/bluethon

from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()
router.register(r'sprints', views.SprintViewSet)
router.register(r'tasks', views.TaskViewSet)
router.register(r'users', views.UserViewSet)
