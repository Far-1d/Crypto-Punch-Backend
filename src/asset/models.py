from django.db import models
from account.models import User

# Create your models here.
class Exchange(models.Model):
    name = models.CharField(max_length=64, unique=True, blank=False)
    url = models.URLField(max_length=256)
    established = models.CharField(max_length=12, null=True, blank=True)
    country = models.CharField(max_length=128, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    image = models.URLField(max_length=2000, blank=True, null=True)
    daily_volume = models.FloatField(blank=True, null=True)
    last_update = models.DateField(auto_now=True)
    trust_score = models.FloatField(blank=True, null=True)
    trust_rank = models.IntegerField(blank=True, null=True)
    class Meta:
        ordering = ['-daily_volume']
        indexes = [
            models.Index(fields=['daily_volume']),
            models.Index(fields=['name'])
        ]

    def __str__(self) -> str:
        return self.name

class Asset(models.Model):
    name = models.CharField(max_length=50, blank=False)
    symbol = models.CharField(max_length=20, blank=True, null=True)
    price = models.FloatField()
    rank = models.IntegerField(blank=True, null=True)
    daily_change = models.FloatField(null=True, blank=True)
    total_volume = models.FloatField(null=True, blank=True)
    icon = models.URLField(max_length=1000, null=True, blank=True) 
    users_interested = models.ManyToManyField(User, related_name='assets', blank=True)
    market_cap = models.FloatField(null=True, blank=True)
    twitter = models.URLField(max_length=512, blank=True, null=True)
    exchanges = models.ManyToManyField(Exchange, 
                                       related_name="assets",
                                       blank=False)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    description = models.TextField(blank=True, null=True)
    
    fully_diluted_valuation = models.FloatField(null=True, blank=True)
    high_24h = models.FloatField(null=True, blank=True)
    low_24h = models.FloatField(null=True, blank=True)
    price_change_percentage_24h = models.FloatField(null=True, blank=True)
    circulating_supply = models.FloatField(null=True, blank=True)
    ath = models.FloatField(null=True, blank=True)
    ath_change_percentage = models.FloatField(null=True, blank=True)
    ath_date = models.DateTimeField(null=True, blank=True)
    atl = models.FloatField(null=True, blank=True)
    atl_change_percentage = models.FloatField(null=True, blank=True)
    atl_date = models.DateTimeField(null=True, blank=True)
     
    class Meta:
        ordering = ['rank']
        indexes = [
            models.Index(fields=['name', 'symbol']),
            models.Index(fields=['daily_change'])
        ]

    def __str__(self) -> str:
        return self.name
    