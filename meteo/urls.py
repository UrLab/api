from django.conf.urls import patterns, include, url
from .views import view_weather

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', view_weather, name='weather'),
)
