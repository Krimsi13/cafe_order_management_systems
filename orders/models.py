from django.db import models


class Item(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название блюда')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Блюдо и цена'
        verbose_name_plural = 'Блюда и цены'


class Order(models.Model):
    STATUS_CHOICES = [
        ('waiting', 'В ожидании'),
        ('ready', 'Готово'),
        ('paid', 'Оплачено'),
    ]
    
    table_name = models.CharField(max_length=50, verbose_name='Номер стола')
    items = models.ManyToManyField(Item, verbose_name='Список заказанных блюд с ценами')  # Связь с моделью Item
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name='Стоимость заказа')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='waiting', verbose_name='Статус заказа')
    
    # Вычисление общей стоимости заказа
    def save(self, *args, **kwargs):
        self.total_price = sum(item.price for item in self.items.all())
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Order {self.id} - Table {self.table_name} - Status: {self.status}"
    
    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
