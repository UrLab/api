from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'meteo.views.today', name='weather_today'),
    url(r'^today$', 'meteo.views.today', name='weather_today'),
    url(r'^thisweek$', 'meteo.views.thisweek', name='weather_thisweek'),
    url(r'^view$', 'meteo.views.weather', name='weather'),
)
