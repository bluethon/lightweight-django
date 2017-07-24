#!/usr/bin/env python3
# encoding: utf-8
# @Date     : 2017-07-23 14:24
# @Author   : Bluethon (j5088794@gmail.com)
# @Link     : http://github.com/bluethon
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.reverse import reverse

from .models import Sprint, Task

User = get_user_model()


class SprintSerializer(serializers.HyperlinkedModelSerializer):
    links = serializers.SerializerMethodField()
    
    class Meta:
        model = Sprint
        # fields = ('id', 'name', 'description', 'end', 'links',)
        fields = '__all__'
    
    def get_links(self, obj):
        request = self.context['request']
        return {
            'self': reverse('sprint-detail', kwargs={'pk': obj.pk}, request=request)
        }


class TaskSerializer(serializers.ModelSerializer):
    assigned = serializers.SlugRelatedField(
        slug_field=User.USERNAME_FIELD, required=False, allow_null=True,
        queryset=User.objects.all())
    status_display = serializers.SerializerMethodField()
    links = serializers.SerializerMethodField()
    
    class Meta:
        model = Task
        fields = ('id', 'name', 'description', 'sprint',
                  'status', 'status_display', 'order',
                  'assigned', 'started', 'due', 'completed', 'links', 'url', )
    
    # noinspection PyMethodMayBeStatic
    def get_status_display(self, obj):
        return obj.get_status_display()
    
    def get_links(self, obj):
        request = self.context['request']
        links = {
            'self': reverse('task-detail', kwargs={'pk': obj.pk}, request=request),
            'sprint': None,
            'assigned': None,
        }
        if obj.sprint_id:
            links['sprint'] = reverse('sprint-detail', kwargs={'pk': obj.sprint_id}, request=request)
        if obj.assigned:
            links['assigned'] = reverse('user-detail', kwargs={User.USERNAME_FIELD: obj.assigned}, request=request)
        
        return links


# class UserSerializer(serializers.HyperlinkedModelSerializer):
class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='get_full_name', read_only=True)
    links = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ('id', User.USERNAME_FIELD, 'full_name', 'is_active', 'links', 'url',)
        extra_kwargs = {
            'url': {'lookup_field': User.USERNAME_FIELD, },
        }
    
    def get_links(self, obj):
        request = self.context['request']
        username = obj.get_username()
        return {
            'self': reverse('user-detail', kwargs={User.USERNAME_FIELD: username}, request=request)
        }
