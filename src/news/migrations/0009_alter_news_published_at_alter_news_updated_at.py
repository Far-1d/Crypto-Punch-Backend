# Generated by Django 5.0.6 on 2024-08-22 10:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0008_alter_news_writer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='published_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='news',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
