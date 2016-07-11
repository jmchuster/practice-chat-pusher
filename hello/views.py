from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
from pusher import Pusher
import os
from datetime import datetime

from .models import Greeting

class JsonStatus:
    def Ok(message = '', data = {}):
        return JsonResponse({**data, **{'status': 'OK', 'message': message}})

    def Noop(message = '', data = {}):
        return JsonResponse({**data, **{'status': 'NOOP', 'message': message}})

    def Error(message = '', data = {}):
        return JsonResponse({**data, **{'status': 'ERROR', 'message': message}})

# Create your views here.
def index(request):
    # return HttpResponse('Hello from Python!')
    return render(request, 'index.html')

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
          app_id = os.environ.get('PUSHER_APP_ID'),
          key = os.environ.get('PUSHER_APP_KEY'),
          secret = os.environ.get('PUSHER_APP_SECRET')
        )

        pusher.trigger('chat_channel', 'message_event', {
            'username': username,
            'message': message,
            'timestamp': datetime.utcnow().isoformat()
        })
        return JsonStatus.Ok()

def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, 'db.html', {'greetings': greetings})
