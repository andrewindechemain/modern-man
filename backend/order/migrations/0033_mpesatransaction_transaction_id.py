# Generated by Django 5.0.6 on 2024-05-29 14:32

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0032_mpesatransaction_delete_buttonimages'),
    ]

    operations = [
        migrations.AddField(
            model_name='mpesatransaction',
            name='transaction_id',
            field=models.CharField(default=uuid.uuid4, max_length=100, unique=True),
        ),
    ]
