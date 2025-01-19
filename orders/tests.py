import json
from django.test import TestCase, Client
from django.urls import reverse
from orders.models import Item, Order
from orders.forms import OrderAddItemsForm

class OrderCreateViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.item1 = Item.objects.create(name='Пицца Маргарита', price=500.00)
        cls.item2 = Item.objects.create(name='Салат Цезарь', price=300.00)
        cls.invalid_item_id = 100  # ID несуществующего товара
    
    def test_get_create_view(self):
        url = reverse('orders:order_create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'orders/order_form.html')
        self.assertIsInstance(response.context['form'], OrderAddItemsForm)
    
    def test_post_create_view_with_valid_items(self):
        data = {
            'table_name': 'Table 1',
            'selected_items': [str(self.item1.pk), str(self.item2.pk)],
        }
        url = reverse('orders:order_create')
        response = self.client.post(url, data)
        self.assertRedirects(response, reverse('orders:order_list'))
        order = Order.objects.last()
        self.assertEqual(order.table_name, 'Table 1')
        self.assertEqual(len(order.items), 2)  # Убираем json.loads(), так как items уже является списком
        self.assertIn({'name': 'Пицца Маргарита', 'price': 500.00}, order.items)
        self.assertIn({'name': 'Салат Цезарь', 'price': 300.00}, order.items)
        self.assertEqual(order.total_price, 800.00)
    
    def test_post_create_view_without_items(self):
        data = {
            'table_name': 'Table 1',
            'selected_items': [],
        }
        url = reverse('orders:order_create')
        response = self.client.post(url, data)
        self.assertRedirects(response, reverse('orders:order_list'))
        order = Order.objects.last()
        self.assertEqual(order.table_name, 'Table 1')
        self.assertEqual(order.items, [])
        self.assertEqual(order.total_price, 0.00)
