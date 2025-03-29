from django.db import models

class CartItem(models.Model):
    customer_id = models.IntegerField()
    product_id = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Customer {self.customer_id} - Product {self.product_id} - {self.quantity}"
