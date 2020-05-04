from django.db import models

class Person(models.Model):
    first_name = models.CharField(verbose_name='firstname', max_length=21)
    last_name = models.CharField(verbose_name='lastname', max_length=21)
    email = models.EmailField(verbose_name='email', blank=True, null=True)

    class Meta:
        ordering = ['first_name']  # Ascending order
        verbose_name = 'Person model'

    def __str__(self):
        return self.first_name+' '+self.last_name

class Address(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    street = models.CharField(max_length=21, blank=True, null=True)
    village = models.CharField(max_length=21, blank=True, null=True)
    city = models.CharField(max_length=21, blank=False, null=False)
    mandal = models.CharField(max_length=21,  blank=True, null=True)
    dist = models.CharField(max_length=21,  blank=True, null=True)
    state = models.CharField(max_length=21,  blank=False, null=False)
    pincode = models.IntegerField(blank=False, null=False)

    class Meta:
        ordering = ['-state']  # Descending order
        verbose_name = 'Address model'

    def __str__(self):
        return self.person.first_name+' '+self.city+' '+self.state

class Musician(models.Model):
    first_name = models.CharField(max_length=21)
    last_name = models.CharField(max_length=21, blank=True, null=False)
    instrument = models.CharField(max_length=30)

    class Meta:
        ordering = ['instrument']
        verbose_name_plural = 'Musician model'

    def __str__(self):
        return self.first_name+' '+self.last_name

class Album(models.Model):
    musician = models.ForeignKey(Musician, on_delete=models.CASCADE)
    #cover_image = models.ImageField(blank=True, null = True, width_field=5, height_field=5)
    name = models.CharField(max_length=50)
    release_date = models.DateField()
    num_stars = models.IntegerField()

    class Meta:
        order_with_respect_to = 'musician'   # Should pass a ForeignKey field
        # ordering = ['name']  # Practice.Album: (models.E021) 'ordering' and 'order_with_respect_to' cannot be used together.
        verbose_name = 'Album model'


    def __str__(self):
        return self.musician.first_name+' '+self.name

class Customer(models.Model):
    SHIRT_SIZE = (('S', 'Small'), ('M', 'Medium'), ('L', 'Large'))
    #Fit_Type = models.TextChoices('FitType', 'SLIM Skinny Regullar')

    name = models.CharField(max_length=21)
    shirt_size = models.CharField(max_length=1, choices=SHIRT_SIZE)
    #fit = models.CharField(choices=Fit_Type.choices, max_length=21)

    class Meta:
        get_latest_by = ['name']
        verbose_name_plural = 'Customer model'

    def __str__(self):
        return self.name



class Topping(models.Model):
    Tname = models.CharField(max_length=50)

    class Meta:
        ordering = ['Tname']
        verbose_name = 'Topping model'

    def __str__(self):
        return self.Tname

class Pizza(models.Model):
    toppings =  models.ManyToManyField(Topping)
    Pname = models.CharField(max_length=50)
    cost = models.DecimalField(max_digits=100, decimal_places=2)

    class Meta:
        ordering = ['Pname']
        verbose_name_plural = 'Pizza model'

    def __str__(self):
        return self.Pname


class Employe(models.Model):
    Efname = models.CharField(max_length=21)
    Elname = models.CharField(max_length=21)

    class Meta:
        ordering = ['-Efname']
        verbose_name = 'Employe model'

    def __str__(self):
        return self.Efname+' '+self.Elname

class Techgroup(models.Model):
    Gname = models.CharField(max_length=21)
    employes = models.ManyToManyField(Employe, through='Onboard')

    class Meta:
        ordering = ['Gname']
        verbose_name = 'Techgroup model'

    def __str__(self):
        return self.Gname

class Onboard(models.Model):
    emp = models.ForeignKey(Employe, on_delete=models.CASCADE)
    grp = models.ForeignKey(Techgroup, on_delete=models.CASCADE)
    date_joined = models.DateField()


    class Meta:
        order_with_respect_to = 'emp'
        verbose_name_plural = 'Onboard model'

    def __str__(self):
        return self.emp.Efname+' '+self.grp.Gname


class Commoninfo(models.Model):
    '''
    This is an abstract model which is used as base calss to add common features to more than one sub
    class model
    '''
    name = models.CharField(max_length=30)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=1, choices=(('M', 'Male'), ('F', 'Female')))
   
    class Meta:
        ordering = ['name']
        abstract = True

class Student(Commoninfo):
    '''
    This sub class model inherts the abstract base class model with attributes.
    '''
    Cgroup = models.CharField(max_length=7)

    class Meta(Commoninfo.Meta):
        '''
        This inherit the base class Meta info
        '''
        db_table = 'student_info'
        verbose_name_plural = 'Student model'

    def __str__(self):
        return self.name+' '+self.Cgroup

class People(models.Model):
    f_name = models.CharField(max_length=30)
    l_name = models.CharField(max_length=30)

    class Meta:
        verbose_name = 'People Model'

    def __str__(self):
        return self.f_name

class Mypeople(People):
    class Meta:
        proxy = True
        ordering = ['f_name']
        verbose_name = 'Mypeople model'

    def anyfunction(self):
        pass

'''Meta Attributes of class Meta:

    Frequently used

        ordering =
            # The default ordering for the object, for use when obtaining lists of objects

        verbose_name =
            # A human-readable name for the object, singular

        verbose_name_plural =
            # A human-readable name for the object, plural

        order_with_respect_to = 
            # Makes this object orderable with respect to the given field, usually a ForeignKey. This can be
            # used to make related objects orderable with respect to a parent object.
             
        get_latest_by = 
            # The name of a field or a list of field names in the model, typically DateField, DateTimeField, or
            # IntegerField. This specifies the default field(s) to use in your model Manager’s latest() and 
            # earliest() methods.

        permissions = 
            # Extra permissions to enter into the permissions table when creating this object. Add, change, 
            # delete, and view permissions are automatically created for each model. 

        db_table = 
            # The name of the database table to use for the model

        indexes = 
            # A list of database indexes that you want to define on the model
    


    Rarely used

        abstract = True           
            # If abstract = True, this model will be an abstract base class.Abstract base classes are useful
            # when you want to put some common information into a number of other models. You write your base
            # class and put abstract=True in the Meta class. This model will then not be used to create any 
            # database table. Instead, when it is used as a base class for other models, its fields will be 
            # added to those of the child class.

        app_label = name of app   
            # If a model is defined outside of an application in INSTALLED_APPS, it must declare which app it
            # belongs to:

        base_manager_name = 
            # 

        db_tablespace = 
            # The name of the database tablespace to use for this model. The default is the project’s 
            # DEFAULT_TABLESPACE setting, if set. If the backend doesn’t support tablespaces, this option
            # is ignored.

        default_manager_name = 
            # The name of the manager to use for the model’s _default_manager.

        default_related_name =

        managed = 
            # Defaults to True, meaning Django will create the appropriate database tables in migrate or as 
            # part of migrations and remove them as part of a flush management command. That is, Django
            # manages the database tables’ lifecycles.If False, no database table creation or deletion 
            # operations will be performed for this model. This is useful if the model represents an existing
            # table or a database view that has been created by some other means. This is the only difference 
            # when managed=False. All other aspects of model handling are exactly the same as normal.

        default_permissions = 
            # Defaults to ('add', 'change', 'delete', 'view'). You may customize this list, for example, by 
            # setting this to an empty list if your app doesn’t require any of the default permissions. 
            # It must be specified on the model before the model is created by migrate in order to prevent 
            # any omitted permissions from being created.

        proxy = 
            # If proxy = True, a model which subclasses another model will be treated as a proxy model.

        required_db_features =
            # List of database features that the current connection should have so that the model is considered
            # during the migration phase. For example, if you set this list to ['gis_enabled'], the model will 
            # only be synchronized on GIS-enabled databases.

        required_db_vendor = 
            # Name of a supported database vendor that this model is specific to. Current built-in vendor names
            # are: sqlite, postgresql, mysql, oracle.

        select_on_save = 
        unique_together =
        index_together =
        constraints = # This is new in Django 2.2'''



class Blog(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Blog Model'
    
    def __str__(self):
        return self.name

class Author(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(blank=True, null=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Author Model'
    
    def __str__(self):
        return self.name


class Entry(models.Model):
    blog = models.ForeignKey(Blog, on_delete = models.CASCADE)
    authors = models.ManyToManyField(Author)
    headline = models.CharField(max_length=255)
    body_text = models.TextField()
    pub_date = models.DateField()
    mod_date = models.DateField()

    class Meta:
        ordering = ['pub_date']
        get_latest_by = 'pub_date'
        verbose_name_plural = 'Entry Model'
    
    def __str__(self):
        return self.headline




# Models for Practicing Querying
class Language(models.Model):
    lang_name = models.CharField(max_length=30)

    def __str__(self):
        return self.lang_name

class Framework(models.Model):
    frame_name = models.CharField(max_length=30)
    frame_lang = models.ForeignKey(Language, on_delete = models.CASCADE)

    def __str__(self):
        return self.frame_name