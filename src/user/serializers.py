from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
    message = serializers.CharField(required=True)
    token = serializers.CharField(required=True)
