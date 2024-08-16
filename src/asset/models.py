from django.db import models
from account.models import User

# Create your models here.
class Exchange(models.Model):
    name = models.CharField(max_length=64, unique=True, blank=False)
    url = models.URLField(max_length=256)
    image = models.URLField(max_length=2000, blank=True, null=True)
    daily_volume = models.FloatField(blank=True, null=True)
    last_update = models.DateField(auto_now=True)
    
    class Meta:
        ordering = ['-daily_volume']
        indexes = [
            models.Index(fields=['-daily_volume']),
            models.Index(fields=['name'])
        ]

    def __str__(self) -> str:
        return self.name

class Asset(models.Model):
    name = models.CharField(max_length=50, blank=False)
    symbol = models.CharField(max_length=10, blank=True, null=True)
    price = models.DecimalField(max_digits=15, decimal_places=7)
    rank = models.IntegerField()
    daily_change = models.DecimalField(max_digits=5, decimal_places=2)
    icon = models.URLField(max_length=1000, null=True, blank=True) 
    users_interested = models.ManyToManyField(User, related_name='assets', blank=True)
    market_cap = models.DecimalField(max_digits=15, decimal_places=3)
    twitter = models.URLField(max_length=512, blank=True, null=True)
    exchanges = models.ManyToManyField(Exchange, 
                                       related_name="assets",
                                       blank=False)
    created_at = models.DateField(auto_now_add=True)
    description = models.TextField(blank=True, null=True)
    
    class Meta:
        ordering = ['-rank']
        indexes = [
            models.Index(fields=['-rank']),
            models.Index(fields=['name', 'symbol']),
            models.Index(fields=['daily_change'])
        ]

    def __str__(self) -> str:
        return self.name
    