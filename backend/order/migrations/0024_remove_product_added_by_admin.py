# Generated by Django 5.0.6 on 2024-05-20 07:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0023_remove_product_discount_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='added_by_admin',
        ),
    ]
