# Generated by Django 5.0.6 on 2024-05-20 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0027_alter_product_discount_percentage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='discount_percentage',
            field=models.PositiveIntegerField(default=0, help_text='Percentage of the discount'),
        ),
    ]
