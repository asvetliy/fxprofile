from rest_framework import serializers


class KafkaSerializer(serializers.BaseSerializer):
    VERSION = 1
    MESSAGE_TYPE = 'pamm'

    def to_representation(self, instance):
        return {'value': instance.value}

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    def to_internal_value(self, data):
        pass
