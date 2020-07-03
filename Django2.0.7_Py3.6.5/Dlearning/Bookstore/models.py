from django.db import models
from django.urls import reverse
from datetime import datetime

class Author(models.Model):
    name = models.CharField(max_length=50, blank=False, null = False)
    email = models.EmailField(max_length=150, blank=True, null = True)
    age = models.IntegerField()

    class Meta:
        ordering = ['-name']
        verbose_name_plural = 'Book Author'
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('authors-name', kwargs={"authorname":self.name}) 
      
class Publisher(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False)
    
    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Book Publisher'
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('publishers-name', kwargs={"pubname":self.name})
    

class Book(models.Model):
    author = models.ManyToManyField(Author, verbose_name='author name', help_text = 'press ctl and select more authors')
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE, verbose_name='publisher name')
    name = models.CharField(max_length=50, blank=False, null=False, verbose_name='book name')
    pages = models.IntegerField(verbose_name='number of pages')
    price = models.DecimalField(max_digits=30, decimal_places=2, verbose_name='price')
    rating = models.FloatField(verbose_name='rating')
    pubdate = models.DateTimeField(default = datetime.now(), verbose_name='published date')
    
    
    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Book'
        db_table = 'book_detail'
        
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('books-name', kwargs={"bookname":self.name})    # key name should be same as in the url argument
    
class Store(models.Model):
    name = models.CharField(max_length=300)
    books = models.ManyToManyField(Book)
    
    
    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Book Store'
        db_table = 'book_store'
        
    def __str__(self):
        return self.name
    
    

class Cityinfo(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False)
    population = models.IntegerField()
    citymanager = models.Manager()
    
    class Meta:
        ordering = ['population']
        verbose_name_plural = 'Cityinfo'
        db_table = 'city_information'
    
    def __str__(self):
        return self.name
    
class Stateinfo(models.Model):
    
    class statemanager(models.Manager):
        
        def all_with_cnt(self):
            from django.db import connection
            with connection.cursor() as cur:
                cur.execute('select * from state_information')
                result_list = []
                for row in cur.fetchall():
                    record = self.model(id=row[0], name=row[1], population=row[2])
                    
                    result_list.append(record)
            
            return result_list, len(result_list)
    
    
    name = models.CharField(max_length=50, blank=False, null=False)
    population = models.IntegerField()
    modelmanager = statemanager()
    
    class Meta:
        ordering = ['population']
        verbose_name_plural = 'State info'
        db_table = 'state_information'
        
    def __str__(self):
        return self.name
    


class Countryinfo(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False)
    code = models.CharField(max_length=7, blank=True, null=True)
    population = models.IntegerField()
    
    class Meta:
        ordering = ['code']
        verbose_name_plural = 'Country info'
        db_table = 'country_information'
        
    def save(self, *args, **kwargs):
        res = input("Do you want to continue with save?")
        
        if res in ['Y', 'y', 'yes', 'Yes', 'YES']:
            super().save(*args, **kwargs)
            
    def __str__(self):
        return self.name       
            


class Movie(models.Model):
    
    class Christ_Nolan_Manager(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(director='Christopher Nolan')
        
    class James_Cameron_Manager(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(director='James Cameron')
            
    
    title = models.CharField(max_length=70, blank=False, null=False)
    director = models.CharField(max_length=50, blank=False, null=False)
    releasedate = models.DateField()
    
    movieslist = models.Manager()
    nolanlist = Christ_Nolan_Manager()
    cameronlist = James_Cameron_Manager()
    
    class Meta:
        ordering = ['releasedate']
        verbose_name_plural = 'Movies info'
        db_table = 'movies_list'
        
    def __str__(self):
        return self.title


class Vichel(models.Model):
    name = models.CharField(max_length=50)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='vichel')
    
    class Meta:
        ordering = ['name']
        
    def __str__(self):
        return self.name
    
    


from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)