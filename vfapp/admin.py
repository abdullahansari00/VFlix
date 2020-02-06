from django.contrib import admin
from .models import MoviesList, MoviesSuggestions
# Register your models here.
admin.site.register(MoviesList)
admin.site.register(MoviesSuggestions)