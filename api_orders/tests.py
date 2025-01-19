from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from orders.models import Item, Order
from api_orders.serializers import OrderSerializer


class OrderSearchApiTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.item1 = Item.objects.create(name='Пицца Маргарита', price=500.00)
        cls.item2 = Item.objects.create(name='Салат Цезарь', price=300.00)

        cls.order1 = Order.objects.create(
            table_name='Table 1',
            items=[{'name': 'Пицца Маргарита', 'price': 500.00}]
        )
        cls.order1.status = 'waiting'
        cls.order1.save()

        cls.order2 = Order.objects.create(
            table_name='Table 2',
            items=[{'name': 'Салат Цезарь', 'price': 300.00}]
        )
        cls.order2.status = 'ready'
        cls.order2.save()

    def test_search_by_table_name(self):
        url = reverse('api:api_order_search')
        response = self.client.get(f'{url}?table_name=Table%201')
        self.assertEqual(response.status_code, 200)
        expected_serializer = OrderSerializer(Order.objects.filter(table_name='Table 1'), many=True)
        self.assertEqual(expected_serializer.data, response.json())

    def test_search_by_status(self):
        url = reverse('api:api_order_search')
        response = self.client.get(f'{url}?status=waiting')
        self.assertEqual(response.status_code, 200)
        expected_serializer = OrderSerializer(Order.objects.filter(status='waiting'), many=True)
        self.assertEqual(expected_serializer.data, response.json())

    def test_search_by_both_params(self):
        url = reverse('api:api_order_search')
        response = self.client.get(f'{url}?table_name=Table%202&status=ready')
        self.assertEqual(response.status_code, 200)
        expected_serializer = OrderSerializer(Order.objects.filter(table_name='Table 2').filter(status='ready'), many=True)
        self.assertEqual(expected_serializer.data, response.json())

    def test_no_results(self):
        url = reverse('api:api_order_search')
        response = self.client.get(f'{url}?table_name=Nonexistent&status=pending')
        self.assertEqual(response.status_code, 400)
        