# Generated by Django 5.0.6 on 2024-05-19 16:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0021_product_is_discounted'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='is_discounted',
        ),
    ]