# Generated by Django 4.0.6 on 2022-07-09 00:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RIO',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('percentage', models.FloatField(default=0)),
            ],
            options={
                'verbose_name': 'Rio',
                'verbose_name_plural': 'Rios',
            },
        ),
        migrations.CreateModel(
            name='InvestmentPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, help_text='Description of the investment', null=True)),
                ('range_amt', models.CharField(blank=True, help_text='Range of investment amount. eg: 100-500', max_length=100, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('rio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rio', to='investment.rio')),
            ],
            options={
                'verbose_name': 'Investment Plan',
                'verbose_name_plural': 'Investments Plans',
            },
        ),
    ]
