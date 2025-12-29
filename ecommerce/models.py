from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):
    cid=models.AutoField(primary_key=True)
    cname=models.CharField(max_length=50)

    def __str__(self):
        return self.cname

class Product(models.Model):
    pid=models.AutoField(primary_key=True)
    pname=models.CharField(max_length=50)
    pdis=models.TextField()
    pprice=models.FloatField()
    pimage=models.ImageField(upload_to='product')
    cat=models.ForeignKey(Category,on_delete=models.CASCADE)

    def __str__(self):
        return self.pname 
    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.user.username} - {self.product.pname}"

    def total_price(self):
        return self.product.pprice * self.quantity


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    mobile = models.CharField(max_length=20)
    address1 = models.CharField(max_length=255)
    address2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=20)
    country = models.CharField(max_length=50, default="United States")
    payment_method = models.CharField(max_length=50)
    total_amount = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default="Pending")

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.FloatField()

    def __str__(self):
        return f"{self.product.pname} × {self.quantity}"

