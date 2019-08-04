from django.conf.urls import url
from django.urls import path
from . import views
from django.contrib.auth.views import (
        PasswordResetView, PasswordResetDoneView,
        PasswordResetConfirmView, PasswordResetCompleteView
    )

urlpatterns = [
    url(r'^$', views.EventListView.as_view(), name = 'index'),
    url(r'^contact/$', views.contact, name = 'contact'),  #This references the views file that points to contact.html which refers to the dictionary in the contact function in views
    url(r'^signup/$', views.signup, name = 'signup'), #This is the Newsletter signup form
    url(r'^login/$', views.gro_login, name = 'gro_login'),
    url(r'^logout/$', views.gro_logout, name = 'gro_logout'),
    url(r'^create/$', views.create_event, name = 'create_event'),
    url(r'^calendar/$', views.CalendarView.as_view(), name = 'calendar'),
    ##url(r'^change-password/$', views.change_password, name = 'change_password'),
    url(r'^reset-password/$', PasswordResetView.as_view(template_name = 'homepage/password_reset.html'),
        name = 'password_reset'),
    url(r'^reset-password/done/$', PasswordResetDoneView.as_view(template_name = 'homepage/password_reset_done.html'),
        name = 'password_reset_done'),
    url(r'^reset-password/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
        PasswordResetConfirmView.as_view(template_name = 'homepage/password_reset_confirm.html'),
        name = 'password_reset_confirm'),
    url(r'^reset-password/complete/$',
        PasswordResetCompleteView.as_view(template_name = 'homepage/password_reset_complete.html'),
        name = 'password_reset_complete'),
    ##path is a newer function compared to url(); url() maybe obselete in the future; url() takes more regex looking syntax like (?P<year>[0-9]+)
    path('delete/<int:event_id>/', views.delete_event, name='delete-event'),
    ]

