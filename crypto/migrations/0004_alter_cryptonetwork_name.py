# Generated by Django 4.0.6 on 2022-07-09 01:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crypto', '0003_alter_wallets_network'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cryptonetwork',
            name='name',
            field=models.CharField(help_text='Name of the network', max_length=100),
        ),
    ]
