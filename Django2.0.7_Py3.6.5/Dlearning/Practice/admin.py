from django.contrib import admin
from Practice.models import Language, Framework
from Practice.models import Person, Address, Musician, Album, Customer, Topping, Pizza, Employe, Techgroup, Onboard, Student, People, Mypeople, Blog, Author, Entry

admin.site.register(Language)
admin.site.register(Framework)

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
admin.site.register(Blog)
admin.site.register(Author)
admin.site.register(Entry)