from django import forms
from .models import Order, Item


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['table_name', 'items', 'status']


class OrderAddItemsForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['table_name']
    
    selected_items = forms.MultipleChoiceField(
        label="Выберите блюда",
        widget=forms.CheckboxSelectMultiple,
        required=False,
        choices=[]
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['selected_items'].choices = [(item.id, f"{item.name} ({item.price})") for item in
                                                 Item.objects.all()]


class OrderSearchForm(forms.Form):
    table_name = forms.CharField(required=False, label='Номер стола')
    status = forms.ChoiceField(required=False, choices=[
        ('', 'Все'),
        ('waiting', 'В ожидании'),
        ('ready', 'Готово'),
        ('paid', 'Оплачено'),
    ], label='Статус')
