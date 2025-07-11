# Generated by Django 5.2.3 on 2025-06-28 09:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0002_alter_orderitem_color_alter_orderitem_size'),
        ('product', '0008_product_additional_info'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='size',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, related_name='size_items', to='product.size'),
        ),
    ]
