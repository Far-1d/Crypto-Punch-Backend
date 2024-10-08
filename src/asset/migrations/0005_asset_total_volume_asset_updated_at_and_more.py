# Generated by Django 5.0.6 on 2024-08-17 18:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asset', '0004_alter_exchange_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='asset',
            name='total_volume',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='asset',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='asset',
            name='daily_change',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True),
        ),
        migrations.AlterField(
            model_name='asset',
            name='market_cap',
            field=models.DecimalField(blank=True, decimal_places=3, max_digits=15, null=True),
        ),
        migrations.AlterField(
            model_name='asset',
            name='rank',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
