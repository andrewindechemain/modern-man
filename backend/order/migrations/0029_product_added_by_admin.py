# Generated by Django 5.0.6 on 2024-05-20 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0028_alter_product_discount_percentage'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='added_by_admin',
            field=models.BooleanField(default=False),
        ),
    ]
