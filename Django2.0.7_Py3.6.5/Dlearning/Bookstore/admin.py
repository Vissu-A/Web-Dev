from django.contrib import admin

from Bookstore.models import Author, Publisher, Book, Store, Cityinfo, Stateinfo, Countryinfo, Movie, Vichel

class Authoradmin(admin.ModelAdmin):
    list_display = ['name', 'age']
    list_display_links = ['name', 'age']
    list_filter = ['age']
    search_fields = ['name']
    
class Publisheradmin(admin.ModelAdmin):
    list_display = ['name']
    list_display_links = ['name']
    list_filter = ['name']
    search_fields = ['name']

class Bookadmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'rating', 'pubdate']
    list_display_links = ['name', 'price']
    list_filter = ['price', 'rating']
    search_fields = ['name']   
    
class Storeadmin(admin.ModelAdmin):
    list_display = ['name']
    list_display_links = ['name']
    list_filter = ['name']
    search_fields = ['name']
    
class Cityinfoadmin(admin.ModelAdmin):
    list_display = ['name', 'population']
    list_display_links = ['population']
    list_filter = ['name', 'population']
    search_fields = ['name']
    
class Stateinfoadmin(admin.ModelAdmin):
    list_display = ['name', 'population']
    list_display_links = ['population']
    list_filter = ['name', 'population']
    search_fields = ['name']
    
class Countryinfoadmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'population']
    list_display_links = ['code']
    list_filter = ['name', 'code']
    search_fields = ['name', 'code']
    
class Movieadmin(admin.ModelAdmin):
    list_display = ['title', 'director', 'releasedate']
    list_display_links = ['title', 'director']
    list_filter = ['director', 'releasedate']
    search_fields = ['title', 'director']
    
admin.site.register(Author, Authoradmin)
admin.site.register(Publisher, Publisheradmin)
admin.site.register(Book, Bookadmin)
admin.site.register(Store, Storeadmin)
admin.site.register(Cityinfo, Cityinfoadmin)
admin.site.register(Stateinfo, Stateinfoadmin)
admin.site.register(Countryinfo, Countryinfoadmin)
admin.site.register(Movie, Movieadmin)
admin.site.register(Vichel)