from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Task(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    is_complete = models.BooleanField(default=False)
    user = models.ForeignKey(User,on_delete=models.CASCADE, blank=True)

    def __str__(self) -> str:
        return f"{self.title}"


