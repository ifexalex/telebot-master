# Generated by Django 4.0.6 on 2022-07-09 01:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('investment', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='rio',
            name='duration',
            field=models.CharField(choices=[('Daily', 'Daily'), ('Monthly', 'Monthly'), ('Yearly', 'Yearly')], default='Daily', max_length=100),
        ),
    ]
