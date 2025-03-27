from django.db import models

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('en-route', 'En-route'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ]

    PAYMENT_METHODS = [
        ('cod', 'Cash on Delivery'),
        ('transfer', 'Bank Transfer')
    ]

    customer_id = models.IntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, default="cod")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} - {self.status}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product_id = models.CharField(max_length=50)  # MongoDB uses string _id
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Store price at time of order

    def __str__(self):
        return f"Order {self.order.id} - Product {self.product_id}"
