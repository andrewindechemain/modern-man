# Generated by Django 5.0.6 on 2024-05-17 08:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0018_verificationcode'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='is_discounted',
        ),
    ]
