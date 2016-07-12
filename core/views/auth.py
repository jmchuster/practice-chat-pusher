from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
import os
from pusher import Pusher

from util import WrappedUser


@require_http_methods(['POST'])
def auth(request):
    user = WrappedUser(request)

    pusher = Pusher(
        app_id=os.environ.get('PUSHER_APP_ID'),
        key=os.environ.get('PUSHER_APP_KEY'),
        secret=os.environ.get('PUSHER_APP_SECRET')
    )

    auth = pusher.authenticate(
        channel=request.POST.get('channel_name', ''),
        socket_id=request.POST.get('socket_id', ''),
        custom_data={
            'user_id': user.user_id,
            'user_info': user.user_info
        })

    return JsonResponse(auth)
