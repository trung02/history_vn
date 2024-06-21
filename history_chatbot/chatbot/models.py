from django.db import models
from django.contrib.auth.models import User
import uuid
# Create your models here.
class Chat(models.Model):
    id = models.UUIDField(default=uuid.uuid1,primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username}: {self.message}'
