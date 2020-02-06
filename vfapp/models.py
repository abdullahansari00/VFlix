from django.db import models

# Create your models here.
class MoviesList(models.Model):
	rank = models.IntegerField(default = ' ')
	title = models.CharField(max_length = 50, default = ' ')
	genre = models.CharField(max_length = 50, default = ' ')
	description = models.TextField(default = ' ')
	director = models.CharField(max_length = 50, default = ' ')
	actors = models.TextField(default = ' ')
	year = models.IntegerField(default = ' ')
	rating = models.IntegerField(default = ' ')

	def __str__(self):
		return self.title

class MoviesSuggestions(models.Model):
	username = models.CharField(max_length = 50, default = ' ')
	watched_movies = models.TextField(default = '0')
	action = models.IntegerField(default = 0)
	adventure = models.IntegerField(default = 0)
	scifi = models.IntegerField(default = 0)
	mystery = models.IntegerField(default = 0)
	horror = models.IntegerField(default = 0)
	thriller = models.IntegerField(default = 0)
	animation = models.IntegerField(default = 0)
	comedy = models.IntegerField(default = 0)
	family = models.IntegerField(default = 0)
	fantasy = models.IntegerField(default = 0)
	drama = models.IntegerField(default = 0)
	music = models.IntegerField(default = 0)
	biography = models.IntegerField(default = 0)
	romance = models.IntegerField(default = 0)
	history = models.IntegerField(default = 0)
	crime = models.IntegerField(default = 0)
	western = models.IntegerField(default = 0)
	war = models.IntegerField(default = 0)
	musical = models.IntegerField(default = 0)
	sport = models.IntegerField(default = 0)

	def __str__(self):
		return self.username