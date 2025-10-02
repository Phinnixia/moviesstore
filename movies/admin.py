from django.contrib import admin
from .models import Movie, Review, Petition
class MovieAdmin(admin.ModelAdmin):
    ordering = ['name']
    search_fields = ['name']

# Register your models here.
admin.site.register(Movie, MovieAdmin)
admin.site.register(Review)
admin.site.register(Petition)