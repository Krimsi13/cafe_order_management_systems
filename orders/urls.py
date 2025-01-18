from django.urls import path
from .views import (
    OrderListView,
    OrderCreateView,
    OrderUpdateView,
    OrderDeleteView,
    OrderDetailView,
)

urlpatterns = [
    # CRUD
    path('', OrderListView.as_view(), name='order_list'),
    path('create/', OrderCreateView.as_view(), name='order_create'),
    path('edit/<int:pk>/', OrderUpdateView.as_view(), name='order_update'),
    path('delete/<int:pk>/', OrderDeleteView.as_view(), name='order_delete'),
    path('detail/<int:pk>/', OrderDetailView.as_view(), name='order_detail'),
    # search
]
