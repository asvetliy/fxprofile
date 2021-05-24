from rest_framework import serializers as s


class MessageSerializer(s.BaseSerializer):
    MESSAGE_TYPE = 'MESSAGE'

    def to_representation(self, instance):
        return {'value': instance.value}

    def to_internal_value(self, data):
        pass

    def save(self, **kwargs):
        pass


class EventSerializer(s.BaseSerializer):
    MESSAGE_TYPE = 'EVENT'

    def to_representation(self, instance):
        return {'value': instance.value}

    def to_internal_value(self, data):
        pass

    def save(self, **kwargs):
        pass
