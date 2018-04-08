from django.forms import ModelForm
from django import forms
from .models import Order, slot


class OrderForm(ModelForm):
    OPTIONS = (
         ('COD','COD'),
         ('Paytm','Paytm'),
         ('Tej','Tej')
    )

    payment_option = forms.ChoiceField(choices=OPTIONS)
    slot_id = forms.ModelChoiceField(queryset=slot.objects.filter(slot_status="free"))
    start_time = forms.TimeField(required=True)
    end_time=forms.TimeField(required=True)
    
    class Meta:
        model = Order
        fields = ['name','phone','address','start_time','end_time','slot_id','payment_option']