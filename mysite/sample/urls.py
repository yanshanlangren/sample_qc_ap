from django.conf.urls import patterns, url

from sample import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^service', views.service, name='service'),
)
