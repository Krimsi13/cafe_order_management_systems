from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView

from api_orders.serializers import OrderSerializer
from orders.models import Order


class OrderCreateApiView(CreateAPIView):
    """Создание заказа через API"""
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderListApiView(ListAPIView):
    """Список всех заказов через API"""
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class OrderRetrieveApiView(RetrieveAPIView):
    """Один заказ через API"""
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderUpdateApiView(UpdateAPIView):
    """Обновление заказ через API"""
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderDestroyApiView(DestroyAPIView):
    """Удаление заказа через API"""
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    
class OrderSearchApiView(ListAPIView):
    """Поиск заказов по номеру стола и статусу"""
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['table_name', 'status']
