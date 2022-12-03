# Generated by Django 4.0.6 on 2022-07-24 01:00

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_alter_telegramuser_message_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='telegramuser',
            name='bot_message_id',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=255, null=True), default=list, size=None),
        ),
    ]
