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
