from rest_framework import serializers

from netbox.api.serializers import NetBoxModelSerializer
from ..models import AppSystem, AppSystemAssignment
from drf_yasg.utils import swagger_serializer_method
from core.models import ObjectType
from netbox.api.fields import ContentTypeField
from utilities.api import get_serializer_for_model


class AppSystemSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_app_systems-api:appsystem-detail')

    class Meta:
        model = AppSystem
        fields = ('id', 'slug', 'url', 'display', 'name', "description",
                  'comments', 'tags', 'custom_fields', 'created', 'last_updated')
        brief_fields = ('id', 'slug', 'url', 'display', 'name')


class AppSystemAssignmentSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_app_systems-api:appsystemassignment-detail')
    object_type = ContentTypeField(
        queryset=ObjectType.objects.all()
    )
    object = serializers.SerializerMethodField(read_only=True)
    app_system = AppSystemSerializer(nested=True)

    class Meta:
        model = AppSystemAssignment
        fields = [
            'id', 'url', 'display', 'object_type', 'object_id', 'object', 'app_system', 'created',
            'last_updated',
        ]
        brief_fields = ['id', 'url', 'display', 'app_system',
                  'object_type', 'object_id']

    @swagger_serializer_method(serializer_or_field=serializers.DictField)
    def get_object(self, instance):
        serializer = get_serializer_for_model(
            instance.object_type.model_class())
        context = {'request': self.context['request']}
        return serializer(instance.object, nested=True, context=context).data
