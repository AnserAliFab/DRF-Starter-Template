from . import models
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = [
            "first_name",
            "last_name",
            "email",
            "password",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = get_user_model().objects.create(**validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user
    
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = self.context['request'].user
        old_password = data['old_password']
        new_password = data['new_password']
        if not user.check_password(old_password):
            raise ValidationError("Old password is incorrect.")

        user.set_password(new_password)
        user.save()

        return data