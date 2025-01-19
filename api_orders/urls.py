from django.urls import path
from .views import (
    OrderListApiView, OrderCreateApiView, OrderRetrieveApiView, OrderUpdateApiView, OrderDestroyApiView,
    OrderSearchApiView
)

urlpatterns = [
    # CRUD
    path('orders/', OrderListApiView.as_view(), name='api_order_list'),
    path('orders/create/', OrderCreateApiView.as_view(), name='api_order_create'),
    path('orders/detail/<int:pk>/', OrderRetrieveApiView.as_view(), name='api_order_retrieve'),
    path('orders/edit/<int:pk>/', OrderUpdateApiView.as_view(), name='api_order_update'),
    path('orders/delete/<int:pk>/', OrderDestroyApiView.as_view(), name='api_order_delete'),
    # search
    path('orders/search/', OrderSearchApiView.as_view(), name='api_order_search'),
]
