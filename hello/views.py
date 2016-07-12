from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
import os
import uuid
from datetime import datetime
from pusher import Pusher

class JsonStatus:
    def Ok(message='', data={}):
        return JsonResponse({**data, **{'status': 'OK', 'message': message}})

    def Noop(message='', data={}):
        return JsonResponse({**data, **{'status': 'NOOP', 'message': message}})

    def Error(message='', data={}):
        return JsonResponse({**data, **{'status': 'ERROR', 'message': message}})

# Create your views here.
def index(request):
    # return HttpResponse('Hello from Python!')
    # return render(request, 'index.html')
    return redirect('chat')

@require_http_methods(['GET', 'POST'])
def chat(request):
    if request.method == 'GET':
        return render(request, 'chat.html', { 'pusher_app_key': os.environ.get('PUSHER_APP_KEY') })
    elif request.method == 'POST':
        message = request.POST.get('message', '').strip()
        if len(message) == 0:
            return JsonStatus.Noop()

        username = request.POST.get('username', '').strip() or 'anonymous'

        pusher = Pusher(
          app_id=os.environ.get('PUSHER_APP_ID'),
          key=os.environ.get('PUSHER_APP_KEY'),
          secret=os.environ.get('PUSHER_APP_SECRET')
        )

        pusher.trigger('presence-chat_channel', 'message_event', {
            'username': username,
            'message': message,
            'timestamp': datetime.utcnow().isoformat()
        })
        return JsonStatus.Ok()

@require_http_methods(['POST'])
def auth(request):
    pusher = Pusher(
        app_id=os.environ.get('PUSHER_APP_ID'),
        key=os.environ.get('PUSHER_APP_KEY'),
        secret=os.environ.get('PUSHER_APP_SECRET')
    )

    user_id = request.COOKIES.get('user_id') or uuid.uuid4().hex

    auth = pusher.authenticate(
        channel=request.POST.get('channel_name', ''),
        socket_id=request.POST.get('socket_id', ''),
        custom_data={
            'user_id': user_id,
            'user_info': {
                'username': 'anon_' + str(hash(user_id) % 1000) # semi-random number up to 1000
            }
        })

    response = JsonResponse(auth)
    response.set_cookie('user_id', user_id, httponly=True)
    return response
