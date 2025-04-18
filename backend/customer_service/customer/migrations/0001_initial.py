# Generated by Django 3.1.12 on 2025-04-08 02:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(max_length=100)),
                ('lastname', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('username', models.CharField(max_length=100, unique=True)),
                ('password', models.CharField(max_length=128)),
                ('address', models.TextField()),
                ('customer_type', models.CharField(choices=[('regular', 'Regular'), ('premium', 'Premium'), ('business', 'Business')], default='regular', max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='PremiumCustomer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('premium_since', models.DateField()),
                ('discount_rate', models.FloatField(default=0.1)),
                ('customer', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='premium_profile', to='customer.customer')),
            ],
        ),
        migrations.CreateModel(
            name='BusinessCustomer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=255)),
                ('bulk_discount_rate', models.DecimalField(decimal_places=2, max_digits=5)),
                ('customer', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='business_profile', to='customer.customer')),
            ],
        ),
    ]
