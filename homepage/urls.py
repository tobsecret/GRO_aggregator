from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.EventListView.as_view(), name = 'index'),
    url(r'^contact/$', views.contact, name = 'contact'),  #This references the views file that points to contact.html which refers to the dictionary in the contact function in views
    url(r'^signup/$', views.signup, name = 'signup'), #This is the Newsletter signup form
    url(r'^login/$', views.gro_login, name = 'gro_login'),
    url(r'^logout/$', views.gro_logout, name = 'gro_logout'),
    url(r'^create/$', views.create_event, name = 'create_event'),
    url(r'^calendar/$', views.CalendarView.as_view(), name = 'calendar'),
    ]

