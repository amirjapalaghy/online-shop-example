# Generated by Django 5.2.3 on 2025-06-29 19:18

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0008_alter_useraddress_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraddress',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_addresses', to=settings.AUTH_USER_MODEL),
        ),
    ]
