from django.conf.urls import include, url

import core.views

# Examples:
# url(r'^$', 'chat.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    url(r'^public_rooms/(?P<public_room_id>[0-9]+)/messages', core.views.public_room.post, name='public_message'),
    url(r'^auth', core.views.auth, name='auth'),
    url(r'^', core.views.index, name='index'),
]
