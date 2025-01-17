from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from .models import Order, Item
from .forms import OrderAddItemsForm, OrderSearchForm


class OrderListView(ListView):
    """Список всех заказов"""
    model = Order
    template_name = 'orders/order_list.html'
    context_object_name = 'orders'
    extra_context = {
        'title': 'Система управления заказами в кафе'
    }
    form_class = OrderSearchForm
    
    def get_queryset(self):
        queryset = super().get_queryset()
        table_name = self.request.GET.get('table_name', '')
        status = self.request.GET.get('status', '')
        
        if table_name:
            queryset = queryset.filter(table_name__icontains=table_name)
        if status:
            queryset = queryset.filter(status=status)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = OrderSearchForm(self.request.GET)
        return context
    

class OrderDetailView(DetailView):
    """Один заказ"""
    model = Order
    template_name = 'orders/order_detail.html'
    context_object_name = 'order'

    
class OrderCreateView(CreateView):
    """Cоздание заказа"""
    model = Order
    form_class = OrderAddItemsForm
    template_name = 'orders/order_form.html'
    success_url = reverse_lazy('orders:order_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        selected_items = self.request.POST.getlist('selected_items')
        items = []
        for item_id in selected_items:
            try:
                item = Item.objects.get(pk=item_id)
                items.append({
                    'name': item.name,
                    'price': float(item.price),
                })
            except Item.DoesNotExist:
                continue
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
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = self.object
        selected_item_ids = [item.get('id', None) for item in order.items if isinstance(item, dict)]
        context['selected_item_ids'] = selected_item_ids
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        selected_items = self.request.POST.getlist('selected_items')
        status = self.request.POST.get('status')

        # Обновление списка блюд
        new_items = []
        for item_id in selected_items:
            try:
                item = Item.objects.get(pk=item_id)
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
    success_url = reverse_lazy('order_list')
