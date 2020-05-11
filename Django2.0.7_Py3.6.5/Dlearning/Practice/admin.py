from django.contrib import admin
from Practice.models import Language, Framework
from Practice.models import Person, Address, Musician, Album, Customer, Topping, Pizza, Employe, Techgroup, Onboard, Student, People, Mypeople, Blog, Author, Entry

class frameadmin(admin.ModelAdmin):
    list_display = ['frame_name', 'frame_lang']
    list_filter = ['frame_lang',]
    #search_fields = ['frame_lang', 'frame_name']
    #prepopulated_fields = {'slug': ('frame_lang','frame_name',)}
admin.site.register(Language)
admin.site.register(Framework, frameadmin)

# Register your models here.
# admin.site.register(Person)
# admin.site.register(Address)
# admin.site.register(Musician)
# admin.site.register(Album)
# admin.site.register(Customer)
# admin.site.register(Topping)
# admin.site.register(Pizza)
# admin.site.register(Employe)
# admin.site.register(Techgroup)
# admin.site.register(Onboard)
# admin.site.register(Student)
# admin.site.register(People)
# admin.site.register(Mypeople)

class Entryadmin(admin.ModelAdmin):
    list_display = ['headline', 'blog', 'pub_date', 'mod_date']
    list_filter = ['blog', 'pub_date', 'mod_date']
    list_display_links = ['headline','blog']
    #list_select_related = ['blog']
    search_fields = ['headline', 'blog']
    
admin.site.register(Blog)
admin.site.register(Author)
admin.site.register(Entry, Entryadmin)