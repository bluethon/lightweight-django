#!/usr/bin/env python3
# encoding: utf-8
# @Date     : 2017-07-26 22:50
# @Author   : Bluethon (j5088794@gmail.com)
# @Link     : http://github.com/bluethon

import django_filters

from django.contrib.auth import get_user_model

from .models import Task


User = get_user_model()


class NullFilter(django_filters.BooleanFilter):
    """ Filter on a field set as null or not. """

    def filter(self, qs, value):
        # qs = query_set
        if value:
            # 使用Django的filter字段特性
            return qs.filter(**{f'{self.name}__isnull': value})
        return qs


class TaskFilter(django_filters.FilterSet):
    backlog = NullFilter(name='sprint')

    class Meta:
        model = Task
        fields = ('sprint', 'status', 'assigned', )             # 不加也自带
        # fields = ('sprint', 'status', 'assigned', 'backlog', )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 已不需要, 自动转换了(!!! 错误, 自动转换
        # Update the assigned filter to use the User.USERNAME_FIELD
        # as the field reference rather than the default pk
        self.filters['assigned'].extra.update(
            {'to_field_name': User.USERNAME_FIELD})
