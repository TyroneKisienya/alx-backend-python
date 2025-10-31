from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    user_id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False, unique=True)
    
class Message(models.Model):
    sender = models.ForeignKey(default=uuid.uuid4)
    receiver = models.ForeignKey(default=uuid.uuid4)
    content = models.TextField(max_length=200)
    timestamp = models.DateTimeField(auto_now_add = True)
