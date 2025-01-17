from django.db import models
from django.db.models import JSONField


# Модель для блюд
class Item(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название блюда')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Блюдо и цена'
        verbose_name_plural = 'Блюда и цены'


# Модель для заказов
class Order(models.Model):
    STATUS_CHOICES = [
        ('waiting', 'В ожидании'),
        ('ready', 'Готово'),
        ('paid', 'Оплачено'),
    ]
    
    table_name = models.CharField(max_length=50, verbose_name='Номер стола')
    items = JSONField(verbose_name='Список заказанных блюд с ценами', null=True, blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name='Стоимость заказа')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='waiting', verbose_name='Статус заказа')
    
    def __str__(self):
        return f"Order {self.id} - Table {self.table_name} - Status: {self.status}"
    
    def get_items(self):
        return "\n".join([f"{item['name']}: {item['price']}" for item in self.items]) if self.items else ""
    
    def save(self, *args, **kwargs):
        self.calculate_total_price()
        super().save(*args, **kwargs)
    
    def calculate_total_price(self):
        if self.items:
            self.total_price = sum(item['price'] for item in self.items)
        else:
            self.total_price = 0.00
    
    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
