from django.views.decorators.http import require_POST
from datetime import datetime

from core.models import PublicRoom
from util import JsonStatus, WrappedUser, WrappedPusher


@require_POST
def post(request, public_room_id):
    room = PublicRoom.objects.get(id=public_room_id)

    message = request.POST.get('message', '').strip()
    if len(message) == 0:
        return JsonStatus.Noop()

    user = WrappedUser(request)
    pusher = WrappedPusher()
    pusher.trigger_message(room.channel, user, message)
    return JsonStatus.Ok()
