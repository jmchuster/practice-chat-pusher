from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from redis import Redis

from util import WrappedPusher, JsonStatus


@csrf_exempt
@require_POST
def presence(request):
    webhook = WrappedPusher().validate_webhook(request)

    channels = []

    for event in webhook['events']:
        if event['name'] == "member_added":
            channels.append(event['channel'])
        elif event['name'] == "member_removed":
            channels.append(event['channel'])

    pusher = WrappedPusher()

    pipeline = Redis().pipeline()

    for channel in set(channels):
        user_count = pusher.channel_count(channel)
        pusher.trigger_public_room_count(channel, user_count)
        pipeline.set(channel, user_count)

    pipeline.execute()

    return JsonStatus.Ok()
