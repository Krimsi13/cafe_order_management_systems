from django.contrib import admin

from orders.models import Order, Item


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "table_name",
        "get_items",
        "total_price",
        "status"
    )
    
@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "price",
    )

