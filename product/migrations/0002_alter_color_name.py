# Generated by Django 5.2.3 on 2025-06-22 18:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='color',
            name='name',
            field=models.CharField(max_length=10),
        ),
    ]
