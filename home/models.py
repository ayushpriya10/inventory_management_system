from django.db import models

# Create your models here.
class Item(models.Model):
    sku = models.CharField(max_length=5, primary_key=True)
    title = models.CharField(max_length=30)
    vendor_ext = models.CharField(max_length=3)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.sku


class Vendor(models.Model):
    extension = models.CharField(max_length=3, primary_key=True)
    name = models.CharField(max_length=30)
    phone = models.CharField(max_length=10)
    website = models.URLField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return self.extension


class Order(models.Model):
    id = models.CharField(max_length=5, primary_key=True)
    cust_name = models.CharField(max_length=30)
    cust_email = models.EmailField()
    item = models.CharField(max_length=60)
    quantity = models.IntegerField()
    shipping_address = models.CharField(max_length=50)
    amount = models.FloatField()
    confirmation = models.CharField(max_length=12, default="Pending")

    def __str__(self):
        return str(self.id)


class User(models.Model):
    username = models.CharField(max_length=20, unique=True)
    email = models.EmailField(primary_key=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    password = models.CharField(max_length=30)

    def __str__(self):
        return self.email
