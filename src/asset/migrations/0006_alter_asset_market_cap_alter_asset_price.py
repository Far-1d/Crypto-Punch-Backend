# Generated by Django 5.0.6 on 2024-08-17 18:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asset', '0005_asset_total_volume_asset_updated_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asset',
            name='market_cap',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='asset',
            name='price',
            field=models.FloatField(),
        ),
    ]
