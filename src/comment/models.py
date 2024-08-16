from django.db import models
from account.models import User
from news.models import News

# Create your models here.
class Comment(models.Model):
    user = models.ForeignKey(User,
                                related_name='comments',
                                null=True,
                                on_delete=models.SET_NULL)
    content = models.TextField()
    news = models.ForeignKey(News, 
                             on_delete=models.CASCADE, 
                             related_name='comments')
    parent = models.ForeignKey('self', 
                               on_delete=models.CASCADE, 
                               null=True, 
                               blank=True, 
                               related_name='replies')
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'Comment by {self.user.username}: {self.text[:20]}'