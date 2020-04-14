import traceback
from venv import logger

from django.shortcuts import render
from django.conf import settings
from rest_auth.utils import jwt_encode
from rest_framework.views import APIView
from rest_auth.registration.views import RegisterView
from rest_auth.app_settings import (TokenSerializer, JWTSerializer, create_token)
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from user_profile.models import Profile


# Create your views here.

class SignupView(RegisterView):
    def create(self, request, format=None):
        input_username = request.data.get('name')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        eixstUser = User.objects.filter(username=input_username).exists()
        # check user existing register else login
        if (eixstUser):
            user = User.objects.get(username=input_username)
        else:
            user = self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)

        return Response(self.get_response_data(user),
                        status=status.HTTP_201_CREATED,
                        headers=headers)

    def perform_create(self, serializer):

        user = serializer.save(self.request)

        if getattr(settings, 'REST_USE_JWT', False):
            self.token = jwt_encode(user)
        else:
            create_token(self.token_model, user, serializer)

        return user

    def get_response_data(self, user):

        try:
            if getattr(settings, 'REST_USE_JWT', False):
                data = {
                    'user': user,
                    'token': self.token
                }
                data = JWTSerializer(data).data
            else:
                data = TokenSerializer(user.auth_token).data

            data.update({'username': user.username})
            return data

        except:
            logger.error('sign up error {}'.format(traceback.format_exc()))


class IsUserExist(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, format=None):

        input_username = request.data.get('username')

        eixstUser = User.objects.filter(username=input_username).exists()

        if (eixstUser):
            return Response({'is_exist': True}, status=status.HTTP_200_OK)
        else:
            return Response({'is_exist': False}, status=status.HTTP_200_OK)


class IsActiveUser(APIView):
    permission_classes = (IsAdminUser,)

    def patch(self, request, *args, **kwargs):
        # print (kwargs.get('pk'))
        user = User.objects.get(id=kwargs.get('pk'))

        if (user.is_active):
            user.is_active = False
        else:
            user.is_active = True
        try:
            user.save()
            return Response({'status': True, 'message': 'user status update success'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status': False, 'message': 'user status update fail'},
                            status=status.HTTP_501_NOT_IMPLEMENTED)


class UpdateUserRole(APIView):
    permission_classes = (IsAdminUser,)

    def patch(self, request, *args, **kwargs):

        profile = Profile.objects.get(id=kwargs.get('pk'))
        profile.role = request.data.get('role')
        profile.news_categories.set(request.data.get('news_categories'))
        try:
            profile.save()
            return Response({'status': True, 'message': 'user role update success'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status': False, 'message': 'user role update fail'},
                            status=status.HTTP_501_NOT_IMPLEMENTED)
