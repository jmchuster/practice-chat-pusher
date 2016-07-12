from django.template.response import TemplateResponse
from django.views.decorators.http import require_http_methods
import os

from util import WrappedUser


@require_http_methods(['GET'])
def index(request):
    user = WrappedUser(request)

    context = {
        'pusher_app_key': os.environ.get('PUSHER_APP_KEY'),
        'user': user
    }
    response = TemplateResponse(request, 'index.html', context)
    user.set_cookie(response)
    return response
