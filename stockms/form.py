import datetime
from django import forms
from customer.models import Customer
from product.models import Product
from purchase.models import Purchase
from stock.models import Stock


class CustomerForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    contact = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    address = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Customer
        fields = ['name', 'contact', 'address']


class ProductForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    brand = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    total_price = forms.FloatField(widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Product
        fields = ['name', 'brand', 'total_price']



class PurchaseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PurchaseForm, self).__init__(*args, **kwargs)
        self.fields['product_id'] = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'form-control'}),
                                                           queryset=Product.objects.all())
        self.fields['customer_id'] = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'form-control'}),
                                                            queryset=Customer.objects.all())

    pieces = forms.FloatField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    price = forms.FloatField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    rate = forms.FloatField(widget=forms.TextInput(attrs={'class': 'form-control', 'onclick': 'multiply()'}))
    date = forms.DateField(initial=datetime.date.today,
                           widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))

    class Meta:
        model = Purchase
        fields = ['product_id', 'customer_id', 'pieces', 'price', 'rate', 'date']


class StockForm(forms.ModelForm):
    quantity = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    sales = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

    # remaining = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        super(StockForm, self).__init__(*args, **kwargs)
        self.fields['product_id'] = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'form-control'}),
                                                           queryset=Product.objects.all())

    class Meta:
        model = Stock
        fields = ['quantity', 'product_id']
