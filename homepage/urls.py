from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name = 'index'),
    url(r'^contact/$', views.contact, name = 'contact'),  #This references the views file that points to contact.html which refers to the dictionary in the contact function in views
    url(r'^signup/$', views.signup, name = 'signup') #This is the Newsletter signup form
    ]
