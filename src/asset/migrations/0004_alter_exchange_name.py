# Generated by Django 5.0.6 on 2024-08-09 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asset', '0003_alter_asset_options_alter_exchange_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exchange',
            name='name',
            field=models.CharField(max_length=64, unique=True),
        ),
    ]
