from django.conf.urls import include, url

import core.views

# Examples:
# url(r'^$', 'chat.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    url(r'^auth', core.views.auth, name='auth'),
    url(r'^', core.views.index, name='index'),
]
