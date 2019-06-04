from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^restaurants/$', views.restaurants, name='restaurants'),
    url(r'^restaurants/(?P<city>.*)/(?P<category>.*)$', views.restaurants, name='restaurants'),
    url(r'^restaurant/(?P<restaurant_number>.*)/', views.restaurant, name='restaurant'),
    url(r'^reservation/$', views.reservation, name='reservation'),
    url(r'^checkout/$', views.checkout, name='checkout'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^reservations/$', views.reservations, name='reservations'),
]
