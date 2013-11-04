from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'meteo.views.today', name='weather_today'),
    url(r'^view$', 'meteo.views.weather', name='weather'),
)
