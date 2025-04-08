from django.db import models

class Customer(models.Model):
    CUSTOMER_TYPES = (
        ('regular', 'Regular'),
        ('premium', 'Premium'),
        ('business', 'Business'),
    )

    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=128)
    address = models.TextField()
    customer_type = models.CharField(max_length=10, choices=CUSTOMER_TYPES, default='regular')

    def __str__(self):
        return f"{self.firstname} {self.lastname} ({self.customer_type})"

class PremiumCustomer(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, related_name='premium_profile')
    premium_since = models.DateField()
    discount_rate = models.FloatField(default=0.10)

class BusinessCustomer(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, related_name='business_profile')
    company_name = models.CharField(max_length=255)
    bulk_discount_rate = models.DecimalField(max_digits=5, decimal_places=2)
