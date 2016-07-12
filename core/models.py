from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField

class Friend(models.Model):
    user = models.ForeignKey(User, related_name='friends')
    friend = models.ForeignKey(User, related_name='+')
    created_at = models.DateTimeField(auto_now_add=True)

class FriendRequest(models.Model):
    user = models.ForeignKey(User, related_name='+')
    desired_friend = models.ForeignKey(User, related_name='friend_requests')
    created_at = models.DateTimeField(auto_now_add=True)

class PublicChannel(models.Model):
    name = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class PublicChannelMessage(models.Model):
    channel = models.ForeignKey(PublicChannel, related_name='messages')
    user = models.TextField()
    timestamp = models.DateTimeField()
    message = models.TextField()

class PrivateChannel(models.Model):
    name = models.TextField()
    created_by = models.ForeignKey(User, related_name='owned_channels')
    users = ArrayField(models.IntegerField()) # models.ForeignKey(user)
    created_at = models.DateTimeField(auto_now_add=True)

class PrivateChannelMessage(models.Model):
    channel = models.ForeignKey(PrivateChannel)
    user = models.TextField()
    timestamp = models.DateTimeField()
    message = models.TextField()

class PrivateChatMessage(models.Model):
    from_user = models.ForeignKey(User, related_name='+')
    to_user = models.ForeignKey(User, related_name='+')
    timestamp = models.DateTimeField()
