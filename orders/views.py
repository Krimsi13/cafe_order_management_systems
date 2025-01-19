from typing import Any, Dict, List, Optional
from django.db.models.query import QuerySet
from django.http import HttpResponse
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from .models import Order, Item
from .forms import OrderAddItemsForm, OrderSearchForm


class OrderListView(ListView):
    """Список всех заказов"""
    model = Order
    template_name = 'orders/order_list.html'
    context_object_name = 'orders'


class OrderDetailView(DetailView):
    """Один заказ"""
    model = Order
    template_name = 'orders/order_detail.html'
    context_object_name = 'order'


class OrderCreateView(CreateView):
    """Создание заказа"""
    model = Order
    form_class = OrderAddItemsForm
    template_name = 'orders/order_form.html'
    success_url = reverse_lazy('orders:order_list')
    
    def form_valid(self, form: OrderAddItemsForm) -> HttpResponse:
        response: HttpResponse = super().form_valid(form)
        selected_items: List[str] = self.request.POST.getlist('selected_items')
        items: List[Dict[str, Any]] = []
        errors: List[int] = []  # Список для хранения идентификаторов несуществующих товаров
        for item_id in selected_items:
            try:
                item: Item = Item.objects.get(pk=item_id)
                items.append({
                    'name': item.name,
                    'price': float(item.price),
                })
            except Item.DoesNotExist:
                errors.append(int(item_id))
                continue
        if errors:
            messages.error(self.request, f"Следующие товары не найдены: {', '.join(map(str, errors))}")
        
        self.object.items = items
        self.object.calculate_total_price()
        self.object.save()
        return response


class OrderUpdateView(UpdateView):
    """Редактирование заказа"""
    model = Order
    form_class = OrderAddItemsForm
    template_name = 'orders/order_form_update.html'
    success_url = reverse_lazy('orders:order_list')

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context: Dict[str, Any] = super().get_context_data(**kwargs)
        order: Order = self.object
        selected_item_ids: List[Optional[str]] = [item.get('id', None) for item in order.items if isinstance(item, dict)]
        context['selected_item_ids'] = selected_item_ids
        return context

    def form_valid(self, form: OrderAddItemsForm) -> HttpResponse:
        response: HttpResponse = super().form_valid(form)
        selected_items: List[str] = self.request.POST.getlist('selected_items')
        status: Optional[str] = self.request.POST.get('status')

        # Обновление списка блюд
        new_items: List[Dict[str, Any]] = []
        for item_id in selected_items:
            try:
                item: Item = Item.objects.get(pk=item_id)
                new_items.append({
                    'id': str(item.pk),
                    'name': item.name,
                    'price': float(item.price),
                })
            except Item.DoesNotExist:
                continue

        # Обновляем поле items
        self.object.items = new_items
        self.object.calculate_total_price()

        # Обновление статуса
        if status:
            self.object.status = status

        self.object.save()
        return response


class OrderDeleteView(DeleteView):
    """Удаление заказа"""
    model = Order
    template_name = 'orders/order_confirm_delete.html'
    success_url = reverse_lazy('orders:order_list')


class OrderManageListView(ListView):
    """Управление заказами"""
    model = Order
    template_name = 'orders/manage_order_list.html'
    context_object_name = 'orders'
    form_class = OrderSearchForm

    def get_queryset(self) -> QuerySet:
        queryset: QuerySet = super().get_queryset()
        table_name: Optional[str] = self.request.GET.get('table_name', '')
        status: Optional[str] = self.request.GET.get('status', '')

        if table_name:
            queryset = queryset.filter(table_name__icontains=table_name)
        if status:
            queryset = queryset.filter(status=status)

        return queryset

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context: Dict[str, Any] = super().get_context_data(**kwargs)
        context['form'] = OrderSearchForm(self.request.GET)
        return context
    
    
class OrderRevenueListView(ListView):
    """Оплаченные заказы"""
    model = Order
    template_name = 'orders/revenue_order_list.html'
    context_object_name = 'orders'

    def get_queryset(self) -> QuerySet:
        queryset: QuerySet = super().get_queryset()
        return queryset.filter(status='paid')  # Фильтрация оплаченных заказов
