# Generated by Django 3.1.12 on 2025-03-27 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_auto_20250327_1341'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='payment_method',
            field=models.CharField(choices=[('cod', 'Cash on Delivery'), ('transfer', 'Bank Transfer')], default='cod', max_length=20),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='product_id',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='quantity',
            field=models.IntegerField(),
        ),
    ]
