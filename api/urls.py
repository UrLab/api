from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from rest_framework import routers
from wiki import views

router = routers.DefaultRouter()
router.register(r'events', views.EventViewSet)


urlpatterns = patterns('',
    url(r'^music/', include('music.urls')),
    url(r'^', include(router.urls)),
    url(r'^meteo/', include('meteo.urls')),
    # Examples:
    # url(r'^$', 'api.views.home', name='home'),
    # url(r'^api/', include('api.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
 
urlpatterns += staticfiles_urlpatterns()