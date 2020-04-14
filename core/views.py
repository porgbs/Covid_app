from __future__ import unicode_literals

import traceback

from django.shortcuts import render
from django.views.generic import TemplateView

from rest_framework.generics import GenericAPIView
from rest_framework.mixins import (CreateModelMixin, ListModelMixin, DestroyModelMixin,
                                   UpdateModelMixin)

from rest_framework import permissions, authentication, status
from rest_framework.response import Response
from rest_framework import filters

from django_filters.rest_framework import DjangoFilterBackend

from .pagination import PageNumberPagination


# Create your views here.
class BaseAPI(GenericAPIView):
    authentication_classes = (authentication.TokenAuthentication,
                              authentication.SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    pagination_class = PageNumberPagination

    def get_error_response(self):
        return Response(
            {"message": self.message}, status=status.HTTP_400_BAD_REQUEST
        )

    def get_response(self):
        return Response(self.serializer.data, status=status.HTTP_200_OK)

    def get_not_found_response(self):
        return Response(status=status.HTTP_404_NOT_FOUND)

    def get_unexpected_error_response(self):
        return Response({"message": self.message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_no_content_response(self):
        return Response({'message': 'delete success', 'status': 1}, status=status.HTTP_204_NO_CONTENT)

    def get_creation_response(self):
        headers = self.get_success_headers(self.serializer.data)
        return Response(self.serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_empty_success_response(self):
        return Response(status=status.HTTP_200_OK)


class BaseAPIView(GenericAPIView):
    authentication_classes = (authentication.TokenAuthentication,
                              authentication.SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    pagination_class = PageNumberPagination

    def get_error_response(self):
        return Response(
            self.serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )

    def get_response(self):
        return Response(self.serializer.data, status=status.HTTP_200_OK)

    def get_not_found_response(self):
        return Response(status=status.HTTP_404_NOT_FOUND)

    def get_unexpected_error_response(self):
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_no_content_response(self):
        return Response({'message': 'delete success', 'status': 1}, status=status.HTTP_204_NO_CONTENT)

    def get_creation_response(self):
        headers = self.get_success_headers(self.serializer.data)
        return Response(self.serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_empty_success_response(self):
        return Response(status=status.HTTP_200_OK)

    def get(self, request, *args, **kwargs):
        try:
            if 'pk' in kwargs:
                instance = self.get_object()
                self.serializer = self.get_serializer(instance)
                return Response(self.serializer.data)
            queryset = self.filter_queryset(self.queryset)
            paginated_queryset = self.paginate_queryset(queryset)
            self.serializer = self.get_serializer(paginated_queryset, many=True)

            return self.get_paginated_response(self.serializer.data)
        except Exception as err:
            return self.get_unexpected_error_response()


class BaseListCreateAPIView(BaseAPIView, CreateModelMixin):

    def post(self, request, *args, **kwargs):

        try:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                return self.create(request, *args, **kwargs)
            else:
                self.serializer = serializer

                return self.get_error_response()
        except Exception as err:

            self.message = traceback.format_exc()

            return self.get_unexpected_error_response()


class BaseRetrieveUpdateDestroyAPIView(BaseAPIView, UpdateModelMixin, DestroyModelMixin):

    def put(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data)
            if serializer.is_valid():
                return self.update(request, *args, **kwargs)
            else:
                self.serializer = serializer
                return self.get_error_response()
        except Exception as err:
            return self.get_unexpected_error_response()

    def patch(self, request, *args, **kwargs):
        try:
            return self.partial_update(request, *args, **kwargs)
        except Exception as err:
            return self.get_unexpected_error_response()

    def delete(self, request, *args, **kwargs):
        try:
            return self.destroy(request, *args, **kwargs)
        except Exception as err:
            return self.get_unexpected_error_response()
