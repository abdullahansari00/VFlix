from django.conf.urls import include, url
from . import views

urlpatterns = [
	url(r'^enter/$', views.enter, name = 'enter'),
	url(r'^enter/signup$', views.signup, name = 'signup'),
	url(r'^exit/$', views.exit, name = 'exit'),
	url(r'^root/changepassword$', views.changepassword, name = 'changepassword'),
	
	url(r'^$', views.home, name = 'home'),
	url(r'^suggested_movies/$', views.suggested_movies, name = 'suggested_movies'),
	url(r'^watched_movies/$', views.watched_movies, name = 'watched_movies'),
	url(r'^search/$', views.search, name = 'search'),
	url(r'^add_movie/(?P<rank>.*)/(?P<var>.*)$', views.add_movie, name = 'add_movie'),
	url(r'^del_movie/(?P<rank>.*)/(?P<var>.*)$', views.del_movie, name = 'del_movie'),

	#url(r'^movies/$', views.movies, name = 'movies'),
	#url(r'^movies/upload_movies/$', views.upload_movies, name = 'upload_movies'),
]