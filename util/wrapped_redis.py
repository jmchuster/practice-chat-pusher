import os
from redis import Redis


class WrappedRedis:
    def __init__(self):
        self._redis = None

    @staticmethod
    def host():
        return os.environ.get('REDIS_HOST')

    @staticmethod
    def port():
        return os.environ.get('REDIS_PORT')

    @staticmethod
    def password():
        return os.environ.get('REDIS_PASSWORD')

    @property
    def redis(self):
        if not self._redis:
            self._redis = Redis(
                host=self.host(),
                port=self.port(),
                password=self.password()
            )
        return self._redis

    def pipeline(self):
        return self.redis.pipeline()
