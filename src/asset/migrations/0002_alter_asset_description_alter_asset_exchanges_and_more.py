# Generated by Django 5.0.6 on 2024-08-08 16:17

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asset', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='asset',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='asset',
            name='exchanges',
            field=models.ManyToManyField(null=True, related_name='assets', to='asset.exchange'),
        ),
        migrations.AlterField(
            model_name='asset',
            name='icon',
            field=models.URLField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='asset',
            name='twitter',
            field=models.URLField(blank=True, max_length=512, null=True),
        ),
        migrations.AlterField(
            model_name='asset',
            name='users_interested',
            field=models.ManyToManyField(blank=True, null=True, related_name='assets', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='exchange',
            name='daily_volume',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='exchange',
            name='image',
            field=models.URLField(blank=True, max_length=2000, null=True),
        ),
    ]
