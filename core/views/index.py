from django.template.response import TemplateResponse
from django.views.decorators.http import require_GET

from util import WrappedUser, WrappedPusher, WrappedRedis
from core.models import PublicRoom


def add_counts(public_rooms):
    pipeline = WrappedRedis().pipeline()
    for room in public_rooms:
        pipeline.get(room.channel)
    counts = pipeline.execute()

    for room, count in zip(public_rooms, counts):
        room.count = count or 0


@require_GET
def index(request):
    user = WrappedUser(request)

    public_rooms = PublicRoom.objects.all()
    add_counts(public_rooms)

    context = {
        'pusher_app_key': WrappedPusher.key(),
        'user': user,
        'public_rooms': public_rooms,
        'private_rooms': user.private_rooms,
        'friends': user.friends,
        'friend_requests': user.friend_requests
    }
    response = TemplateResponse(request, 'index.html', context)
    user.set_cookie(response)
    return response
