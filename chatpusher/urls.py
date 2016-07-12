from django.conf.urls import include, url

from django.contrib import admin
admin.autodiscover()

import core.views

# Examples:
# url(r'^$', 'chatpusher.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    url(r'^', include('core.urls'))
]
