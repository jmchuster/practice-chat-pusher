from django.template.response import TemplateResponse
from django.views.decorators.http import require_GET

from util import WrappedUser, WrappedPusher
from core.models import PublicRoom

@require_GET
def index(request):
    user = WrappedUser(request)

    context = {
        'pusher_app_key': WrappedPusher.key(),
        'user': user,
        'public_rooms': PublicRoom.objects.all(),
        'private_rooms': user.private_rooms,
        'friends': user.friends,
        'friend_requests': user.friend_requests
    }
    response = TemplateResponse(request, 'index.html', context)
    user.set_cookie(response)
    return response
