from django.conf.urls import url
from . import views

urlpatterns = [
    #url(r'^$', views.post_list, name='post_list'),
	#url(r'^Movies/$', views.movies, name='movies'),
	url(r'^Home', views.home, name='Home'),
	url(r'^Search', views.search, name='Search'),
]