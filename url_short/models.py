from django.db import models
import hashlib
from accounts.models import CustomUser

class URLModel(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    original_url = models.URLField()
    shorten_url = models.CharField(max_length=10,unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    clicks = models.PositiveBigIntegerField(default=0)
    
    class Meta:
        unique_together = ('user', 'original_url')

    def __str__(self):
        return self.shorten_url

