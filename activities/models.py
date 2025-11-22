from django.db import models
from django.conf import settings
from posts.models import Post

class Activity(models.Model):
    TYPE_CHOICES = [("POST", "Post"), ("LIKE", "Like"), ("FOLLOW", "Follow"), ("COMMENT", "Comment")]
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="activities")
    target_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="targeted_activities")
    post = models.ForeignKey(Post, on_delete=models.SET_NULL, null=True, blank=True, related_name="activities")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["-created_at"])]

class Notification(models.Model):
    TYPE_CHOICES = [("LIKE", "Like"), ("FOLLOW", "Follow"), ("COMMENT", "Comment")]
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notifications")
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sent_notifications")
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    post = models.ForeignKey(Post, on_delete=models.SET_NULL, null=True, blank=True, related_name="notifications")
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["recipient", "is_read", "-created_at"])]

# Create your models here.
