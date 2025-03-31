from django.db import models

class Rating(models.Model):
    customer_id = models.IntegerField()
    product_id = models.CharField(max_length=50)  # Matches MongoDB's _id
    rating = models.DecimalField(max_digits=2, decimal_places=1)
    review = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('customer_id', 'product_id')  # Prevent duplicate ratings per user

    def __str__(self):
        return f"Customer {self.customer_id} - Product {self.product_id} - Rating {self.rating}"
