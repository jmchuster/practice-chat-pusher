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
    muted = models.BooleanField(default=False)

    def mute(self):
        self.muted = True
        self.save()


class PublicRoom(models.Model):
    name = models.TextField()
    created_by = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def channel(self):
        return 'presence-public_room.' + str(self.id)

    @property
    def count_channel(self):
        return 'public-public_room_count.' + str(self.id)

class PublicRoomMessage(models.Model):
    channel = models.ForeignKey(PublicRoom, related_name='messages')
    user = models.TextField()
    timestamp = models.DateTimeField()
    message = models.TextField()


class PrivateRoom(models.Model):
    name = models.TextField()
    created_by = models.ForeignKey(User, related_name='owned_rooms')
    users = ArrayField(models.IntegerField())  # models.ForeignKey(user)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def channel(self):
        return 'presence-private_room.' + str(self.id)

    @property
    def count_channel(self):
        return 'private-private_room_count.' + str(self.id)


def private_rooms(self):
    PrivateRoom.objects.filter(users__contains=[self.id])

User.add_to_class('private_rooms', private_rooms)


class PrivateRoomMessage(models.Model):
    channel = models.ForeignKey(PrivateRoom)
    user = models.TextField()
    timestamp = models.DateTimeField()
    message = models.TextField()


class PrivateChatMessage(models.Model):
    from_user = models.ForeignKey(User, related_name='+')
    to_user = models.ForeignKey(User, related_name='+')
    timestamp = models.DateTimeField()
