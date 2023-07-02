from django.db import models
from users.models import User

class Notif(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(blank = True, null = True)
    timestamp = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.user + self.timestamp
