import uuid


class WrappedUser:
    def __init__(self, request):
        self.request = request
        self.user = request.user
        self._user_id = None

    @property
    def username(self):
        if self.is_authenticated:
            return self.user.username
        else:
            return 'anon_' + '{0:03d}'.format(hash(self.user_id) % 1000)  # anon_123

    @property
    def user_id(self):
        if self.is_authenticated:
            return self.user.id
        else:
            if not self._user_id:
                self._user_id = self.request.COOKIES.get('user_id') or uuid.uuid4().hex
            return self._user_id

    @property
    def is_authenticated(self):
        return self.user.is_authenticated()

    @property
    def user_info(self):
        return {
            'username': self.username,
            'user_id': self.user_id,
            'is_authenticated': self.is_authenticated
        }

    @property
    def friends(self):
        if self.is_authenticated:
            return self.user.friends
        else:
            return []

    @property
    def friend_requests(self):
        if self.is_authenticated:
            return self.user.friend_requests
        else:
            return []

    @property
    def private_rooms(self):
        if self.is_authenticated:
            return self.user.private_rooms
        else:
            return []

    @property
    def owned_rooms(self):
        if self.is_authenticated:
            return self.user.owned_rooms
        else:
            return []

    def set_cookie(self, response):
        if not self.is_authenticated:
            response.set_cookie('user_id', self.user_id, httponly=True)
