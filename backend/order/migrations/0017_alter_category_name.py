# Generated by Django 5.0.4 on 2024-05-14 05:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0016_alter_category_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(choices=[('suits', 'Suits'), ('shirts', 'Shirts'), ('neckwear', 'Neckwear & Accessories'), ('shoes', 'Shoes')], max_length=100),
        ),
    ]
