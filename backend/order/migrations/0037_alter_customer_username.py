# Generated by Django 5.0.6 on 2024-06-28 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0036_alter_customer_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='username',
            field=models.CharField(default='Anonymous', max_length=150, unique=True, verbose_name='Username'),
        ),
    ]
