from django.forms import ModelForm, PasswordInput
from .models import Item, Order, Vendor, User

class ItemForm(ModelForm):
    class Meta:
        model = Item
        fields = '__all__'

        labels = {
            'sku':'Product SKU',
            'title':'Product Title',
            'vendor_ext':'Vendor Extension',
            'quantity':'Quantity Available',
            'price':'Price',
        }


class VendorForm(ModelForm):
    class Meta:
        model = Vendor
        fields = '__all__'

        labels = {
            'name':'Vendor Name',
            'extension':'Vendor Extension',
            'phone':'Phone',
            'email':'Email',
            'website':'Website',
        }


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = '__all__'

        labels = {
            'id':'Order ID',
            'cust_name':'Customer Name',
            'cust_email':'Customer Email',
            'shipping_address':'Shipping Address',
            'item':'Item Ordered',
            'quantity':'Quantity',
            'amount':'Total Amount',
        }


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = '__all__'

        labels = {
            'username':'Username',
            'email':'Email',
            'first_name':'First Name',
            'last_name':'Last Name',
            'password':'Password',
        }

        widgets = {
            'password':PasswordInput,
        }
