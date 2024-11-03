from django.db import transaction
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import KeyValue
from .serializers import KeyValueSerializer


class KeyValueViewSet(viewsets.ViewSet):
    @transaction.atomic
    def create(self, request):
        serializer = KeyValueSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @transaction.atomic
    def retrieve(self, request, key=None):
        try:
            kv = KeyValue.objects.get(key=key)
            serializer = KeyValueSerializer(kv)
            return Response(serializer.data)
        except KeyValue.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def update(self, request, key=None):
        try:
            kv = KeyValue.objects.get(key=key)
            serializer = KeyValueSerializer(kv, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except KeyValue.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, key=None):
        try:
            kv = KeyValue.objects.get(key=key)
            kv.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except KeyValue.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        kvs = KeyValue.objects.all()
        serializer = KeyValueSerializer(kvs, many=True)
        return Response(serializer.data)
