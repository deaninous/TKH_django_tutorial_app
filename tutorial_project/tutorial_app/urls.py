from django.conf.urls import patterns, url
from tutorial_app import views

urlpatterns = patterns('',
url(r'^$', views.index, name='index'),
url(r'^about/$', views.about, name='about'),
url(r'^category/(?P<test>[*])$', views.category, name='category'),
url(r'^add_category/$', views.add_category, name='add_category'),
url(r'^category/(?P<test>[*])/add_page/$', views.add_page, name='add_page'),
url(r'^register/$', views.register, name='register'),
url(r'^login/$', views.user_login, name='login'),#new
)