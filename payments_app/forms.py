#from django import forms
from django.forms import ModelForm
from .models import Invoice

NETWORK_CHOICES = [
        ('BTC', 'Bitcoin'),
        ('LTC', 'Litecoin'),
        ('ETH', 'Ethereum'),
        ('BNB', 'BNB'),
        ('MATIC', 'Polygon'),
    ]
CURRENCY_CHOICES = [
        ('BTC', 'Bitcoin'),
        ('LTC', 'Litecoin'),
        ('ETH', 'Ethereum'),
        ('BNB', 'BNB'),
        ('MATIC', 'MATIC'),
    ]
class InvoiceForm(ModelForm):
    #inv_network = forms.CharField(label='Network', widget=forms.Select(choices=NETWORK_CHOICES))
    #inv_currency = forms.CharField(label='Currency', widget=forms.Select(choices=CURRENCY_CHOICES))
    #inv_price = forms.DecimalField()
    class Meta:
        model = Invoice
        fields = ['inv_network', 'inv_currency', 'inv_price']
        labels = {
            "inv_network": "Select network ",
            "inv_currency": "Select currency",
            "inv_price": "Amount to deposit",
        }