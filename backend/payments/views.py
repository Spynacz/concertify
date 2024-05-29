from django.core.cache import cache

from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from payments.serializers import OrderSerializer


def get_cart(id):
    data = cache.get(id)
    if not data:
        return Response({'error': 'No data assigned to the given key.'},
                        status=status.HTTP_400_BAD_REQUEST)
    return data


class ShoppingCartView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        data = get_cart(request.user.id)
        if isinstance(data, Response):
            return data

        serializer = OrderSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = OrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cache.set(request.user.id, serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        serializer = OrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        old_data = cache.get(request.user.id)
        cache.set(request.user.id, serializer.data)

        if old_data:
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        cache.delete(request.user.id)
        return Response(status=status.HTTP_204_NO_CONTENT)


class CheckoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        data = get_cart(request.user.id)
        if isinstance(data, Response):
            return data

        serializer = OrderSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
