# Generated by Django 4.0.6 on 2022-07-09 01:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('investment', '0003_alter_rio_duration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rio',
            name='percentage',
            field=models.IntegerField(default=0),
        ),
    ]
