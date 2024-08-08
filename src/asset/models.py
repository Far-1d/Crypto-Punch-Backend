from django.db import models

# Create your models here.
class Asset(models.Model):
    name = models.CharField(max_length=50, blank=False)
    symbol = models.CharField(max_length=10, blank=True, null=True)
    price = models.DecimalField(max_digits=15, decimal_places=7)
    icon = models.URLField(max_length=1000, null=True)
    users_interested = models.ForeignKey('User', related_name='assets',
                                         on_delete=models.DO_NOTHING)
    created_at = models.DateField(auto_now_add=True)
    description = models.TextField(blank=True)
    
    def __str__(self) -> str:
        return self.name