from django.views.decorators.http import require_POST
from django.http import JsonResponse

from util import WrappedUser, WrappedPusher


@require_POST
def auth(request):
    user = WrappedUser(request)

    pusher = WrappedPusher()
    auth = pusher.authenticate(user, request.POST['channel_name'], request.POST['socket_id'])

    return JsonResponse(auth)
