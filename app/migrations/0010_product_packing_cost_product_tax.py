# Generated by Django 5.0.4 on 2024-04-20 00:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_brand_product_brand'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='packing_cost',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='tax',
            field=models.IntegerField(null=True),
        ),
    ]
