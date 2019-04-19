from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserSession(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, default=None, on_delete=models.CASCADE)
    jwt_token = models.TextField(default='',)
    jwt_token_created = models.DateTimeField(blank=True, null=True, auto_now_add=True)

    def __str__(self):
        return self.user.email
