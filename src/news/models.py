from django.db import models
from account.models import User
from asset.models import Asset
from django.contrib.postgres.search import SearchVector
from ckeditor.fields import RichTextField

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField(null=True, blank=True)
    
    class Meta:
        ordering = ['name']

    def __str__(self) -> str:
        return self.name
    
class News(models.Model):
    title = models.CharField(max_length=255, blank=False, null=False)
    content = RichTextField()
    image = models.CharField(max_length=1000, null=True)
    writer = models.ForeignKey(User,
                               related_name='writen_news',
                               null=True,
                               blank=True,
                               on_delete=models.SET_NULL)
    tags = models.ManyToManyField(Asset,
                             related_name='related_news',
                             blank=True)
    likes = models.ManyToManyField(User, 
                                   related_name='liked_news', 
                                   blank=True)
    published_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=[
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ], default='draft')

    class Meta:
        ordering = ['-published_at']
        indexes = [
            models.Index(fields=['-published_at'])
        ]
        verbose_name = 'News'
        verbose_name_plural = 'News'

    def __str__(self) -> str:
        return self.title