from django.conf.urls import patterns, url
from pamela import views


urlpatterns = patterns('',
    url(r'^$', views.get, name='index')
)
