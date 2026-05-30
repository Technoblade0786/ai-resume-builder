
from django.db import models
from django.contrib.auth.models import User

class Resume(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()     # AI generated resume text
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Resume by {self.user.username} on {self.created_at}"


# Create your models here.
