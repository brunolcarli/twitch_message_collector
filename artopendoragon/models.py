from django.db import models


class ChatMessage(models.Model):
    message_datetime = models.DateTimeField(auto_now_add=True)
    message = models.TextField(null=False, blank=False)
    username = models.CharField(max_length=300, null=False, blank=False)
 