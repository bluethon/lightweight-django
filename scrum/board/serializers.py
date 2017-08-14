#!/usr/bin/env python3
# encoding: utf-8
# @Date     : 2017-07-23 14:24
# @Author   : Bluethon (j5088794@gmail.com)
# @Link     : http://github.com/bluethon

from datetime import date

from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from rest_framework.reverse import reverse

from .models import Sprint, Task

User = get_user_model()


class SprintSerializer(serializers.HyperlinkedModelSerializer):
    links = serializers.SerializerMethodField()     # 冗余, 已由url自动生成
    
    class Meta:
        model = Sprint
        fields = ('id', 'name', 'description', 'end', 'links', 'url',)
        # fields = '__all__'
    
    def get_links(self, obj):
        request = self.context['request']
        return {
            'self': reverse('sprint-detail', kwargs={'pk': obj.pk}, request=request),
            'tasks': reverse('task-list', request=request) + f'?sprint={obj.pk}',
        }

    # def validate_end(self, attrs, source):        # old
    def validate_end(self, value):
        # 截止时间不能是过去
        # end_date = attrs[source]
        # new = not self.object
        # changed = self.object and self.object.end != end_date
        new = self.instance is None
        changed = self.instance and self.instance.end != value
        # if (new or changed) and (end_date < date.today()):
        if (new or changed) and (value < date.today()):
            msg = _('End date cannot be in the past.')
            raise serializers.ValidationError(msg)
        return value


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

    # TODO: need
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

    def validated_sprint(self, value):
        # task完成后, sprint不能再改变
        # task完成后, 不能再分配给sprint
        if self.instance and self.instance.pk:
            if value != self.instance.sprint:
                if self.instance.status == Task.STATUS_DONE:
                    msg = _('Cannot change the sprint of a completed task.')
                    raise serializers.ValidationError(msg)
                if value and value.end < date.today():
                    msg = _('Cannot assign tasks to past sprints.')
                    raise serializers.ValidationError(msg)
        else:
            if value and value.end < date.today():
                msg = _('Cannot add tasks to past sprints.')
                raise serializers.ValidationError(msg)
        return value

    def validate(self, attrs):
        # 仅在api中生效, 后台仍然可以设置不符合此处校验的数据
        sprint = attrs.get('sprint')
        status = attrs.get('status', Task.STATUS_TODO)
        started = attrs.get('started')
        completed = attrs.get('completed')
        if not sprint and status != Task.STATUS_TODO:
            msg = _('Backlog tasks must have "Not Started" status.')
            raise serializers.ValidationError(msg)
        if started and status != Task.STATUS_TODO:
            msg = _('Started date cannot be set for not started tasks.')
            raise serializers.ValidationError(msg)
        if completed and status != Task.STATUS_DONE:
            msg = _('Completed date cannot be set for uncompleted tasks.')
            raise serializers.ValidationError(msg)
        return attrs


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
            'self': reverse('user-detail', kwargs={User.USERNAME_FIELD: username}, request=request),
            'tasks': f"{reverse('task-list', request=request)}?assigned={username}"
        }
