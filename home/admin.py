from django.contrib import admin
from .models import Item, User, Vendor, Order

# Register your models here.
admin.site.register(Item)
admin.site.register(User)
admin.site.register(Vendor)
admin.site.register(Order)
