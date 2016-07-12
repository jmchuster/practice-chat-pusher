from django.conf.urls import include, url

import core.views

# Examples:
# url(r'^$', 'chat.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    url(r'^login', core.views.account.LoginView.as_view(), name='login'),
    url(r'^logout', core.views.account.LogoutView.as_view(), name='logout'),
    url(r'^signup', core.views.account.SignupView.as_view(), name='signup'),
    url(r'^webhook/presence', core.views.webhook.presence),
    url(r'^public_rooms/(?P<public_room_id>[0-9]+)/messages', core.views.public_room.message),
    url(r'^public_rooms', core.views.public_room.new),
    url(r'^auth', core.views.auth),
    url(r'^', core.views.index, name='index'),
]
