from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
from django.contrib.auth import views as auth_views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Microcontrollers.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^records/', include('Receiver.urls', namespace="records")),
    url(r'^', 'django.contrib.auth.views.login', {'template_name': 'index.html'}),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': 'index.html'}),

)



