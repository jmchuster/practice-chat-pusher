import os
from datetime import datetime

from pusher import Pusher


class WrappedPusher:
    def __init__(self):
        self._pusher = None

    @staticmethod
    def app_id():
        return os.environ.get('PUSHER_APP_ID')

    @staticmethod
    def key():
        return os.environ.get('PUSHER_APP_KEY')

    @staticmethod
    def secret():
        return os.environ.get('PUSHER_APP_SECRET')

    @property
    def pusher(self):
        if not self._pusher:
            self._pusher = Pusher(
                app_id=self.app_id(),
                key=self.key(),
                secret=self.secret()
            )
        return self._pusher

    def authenticate(self, user, channel, socket_id, custom_data=None):
        return self.pusher.authenticate(
            channel=channel,
            socket_id=socket_id,
            custom_data={
                'user_id': user.user_id,
                'user_info': user.user_info
            })

    def trigger_message(self, channel, user, message):
        self.pusher.trigger(channel, 'message_event', {
            'username': user.username,
            'message': message,
            'timestamp': datetime.utcnow().isoformat()
        })

    def trigger_public_new_room(self, room):
        self.pusher.trigger('public-public_rooms', 'new_room_event', {
            'id': room.id,
            'name': room.name,
            'channel': room.channel
        })

    # has the room channel, not the room id
    def trigger_public_room_count(self, channel, count):
        self.pusher.trigger('public-public_rooms', 'room_count_event', {
            'channel': channel,
            'count': count
        })

    def validate_webhook(self, request):
        return self.pusher.validate_webhook(
            key=request.META['HTTP_X_PUSHER_KEY'],
            signature=request.META['HTTP_X_PUSHER_SIGNATURE'],
            body=request.body.decode('UTF-8')
        )

    def channel_count(self, channel):
        return self.pusher.channel_info(channel, ['user_count'])['user_count']
