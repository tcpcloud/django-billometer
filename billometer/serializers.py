from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Project


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Group
        fields = ('url', 'name')


class ProjectSerializer(serializers.HyperlinkedModelSerializer):

    pk = serializers.Field()

    class Meta:
        model = Project
        fields = ('pk', 'id', 'name', 'openstack_tenant',
                  'customer_name', 'customer_id', 'extra')
        read_only_fields = ('name', 'openstack_tenant')
