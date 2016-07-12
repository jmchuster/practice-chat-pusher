from django.views.decorators.http import require_POST
from datetime import datetime

from core.models import PublicRoom
from util import JsonStatus, WrappedUser, WrappedPusher


@require_POST
def message(request, public_room_id):
    room = PublicRoom.objects.get(id=public_room_id)

    message = request.POST.get('message', '').strip()
    if len(message) == 0:
        return JsonStatus.Noop()

    user = WrappedUser(request)
    WrappedPusher().trigger_message(room.channel, user, message)
    return JsonStatus.Ok()


def new(request):
    name = request.POST.get('name').strip()
    if len(name) == 0:
        return JsonStatus.Noop()

    user = WrappedUser(request)

    room = PublicRoom()
    room.name = name
    room.created_by = user.username
    room.save()

    WrappedPusher().trigger_public_new_room(room)
    return JsonStatus.Ok()
