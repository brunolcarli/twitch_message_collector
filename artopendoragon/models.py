from django.db import models


class ChatMessage(models.Model):
    message_datetime = models.DateTimeField(auto_now_add=True)
    message = models.TextField(null=False, blank=False)
    username = models.CharField(max_length=300, null=False, blank=False)
    message_sentiment = models.FloatField(default=0)
    message_offense_level = models.FloatField(default=0)
