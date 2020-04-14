from rest_framework import serializers
from rest_auth.registration.serializers import RegisterSerializer
from allauth.account.adapter import get_adapter


class SignupSerializer(RegisterSerializer):
    name = serializers.CharField(max_length=500)
    def custom_signup(self, request, user):

        adapter = get_adapter()
        username = adapter.generate_unique_username([self.validated_data['name']])
        user.username = self.validated_data['name']
        user.save()

