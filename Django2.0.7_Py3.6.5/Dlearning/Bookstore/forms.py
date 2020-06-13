from django import forms
from Bookstore.models import Book, Vichel

from datetime import datetime

from django.contrib.auth import password_validation
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

# class Bookform(Form):
#     author = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), label='Author Name', max_length=30)
#     publisher = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), label='Publisher Name', max_length=50)
#     bookname = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), label='Book Name', max_length=70)
#     pagecnt = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control'}), label='Number of pages')
#     price = forms.DecimalField(widget=forms.NumberInput(attrs={'class':'form-control'}), label='Price', decimal_places=2)
#     rating = forms.FloatField(widget=forms.NumberInput(attrs={'class':'form-control'}), label='Rating')
#     pdate = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'class':'form-control'}), label='Published Date')

class Bookform(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['name', 'author', 'publisher', 'pages', 'price', 'rating', 'pubdate']
        field_classes = {
            'name' : forms.CharField,
            'pages' : forms.IntegerField,
        }
        exclude = []  # fields to exclude in the form
        
        widgets = {
            'name' : forms.TextInput(attrs={'class':'form-control'}),
            'author' : forms.SelectMultiple(attrs={'class':'form-control'}),
            'publisher' : forms.Select(attrs={'class':'form-control'}),
            'pages' : forms.NumberInput(attrs={'class':'form-control'}),
            'price' : forms.NumberInput(attrs={'class':'form-control'}),
            'rating' : forms.NumberInput(attrs={'class':'form-control'}),
            'pubdate' : forms.DateTimeInput(attrs={'class':'form-control'})
        }
        
        labels = {
            'name' : ('Book Title'),
        }
        
        help_texts = {
            'name' : ('Book name should be meaningfull'),
            'publisher' : ('Please select one of the publishers')
        }
        
        error_messages = {
            'rating' : {
                'max_length' : ('rate out of 5'),
            },
            
            'price' : {
                'decimal_places' : ('Round decimal places to 2')
            }
        }
        
        localized_fields = ['pubdate', ]
        


class authorform(forms.Form):
    authname = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), label='Author Name', max_length=50)
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}), label='Email', max_length=70)
    age = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control'}), label='Age')
    
    
    
class Vichelform(forms.ModelForm):
    class Meta:
        model = Vichel
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control'}),
            'cost': forms.NumberInput(attrs={'class':'form-control'}),
            'image': forms.FileInput(attrs={'class':'form-control'}),
        }
        
class userregistrationform(UserCreationForm):
    
    '''
    Here The password1 and password2 fields are taken from the UserCreationForm not from model class.
    username and email are taken from User model.
    applying widgets on the UserCreationForm's attributes(password1, password2)
    will have no effect and use.
    '''
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class':'form-control'}),
            'email': forms.EmailInput(attrs={'class':'form-control'}),
            'password1': forms.PasswordInput(attrs={'class':'form-control'}),
            'password2': forms.PasswordInput(attrs={'class':'form-control'}),
        }



class CustomUserRegistrationForm(forms.ModelForm):
   
    """
    A form that creates a user, with no privileges, from the given username and
    password. This custom registration form is implimented by copying the Default 
    UserRegistrationForm logic. Because applying class attribute in the widgets on password
    fields of subclass extended the UserRegistrationForm like above commented from is 
    not working.
    """
    
    error_messages = {
        'password_mismatch': ('The two passcode fields didn’t match.'),
    }
    
    password1 = forms.CharField(
        label=("Passcode"),
        strip=False,
        widget=forms.PasswordInput(attrs={'class':'form-control', 'autocomplete': 'new-password'}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    
    password2 = forms.CharField(
        label=("Passcode confirmation"),
        widget=forms.PasswordInput(attrs={'class':'form-control', 'autocomplete': 'new-password'}),
        strip=False,
        help_text=("Enter the same password as before, for verification."),
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', ]
        
        widgets = {
            'username': forms.TextInput(attrs={'class':'form-control', 'autofocus':True}),
            'email': forms.EmailInput(attrs={'class':'form-control'}),
        }
        
        labels = {
            'email':('Email'),
        }
        
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2
    
    def _post_clean(self):
        super()._post_clean()
        # Validate the password after self.instance is updated with form data
        # by super().
        password = self.cleaned_data.get('password2')
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except forms.ValidationError as error:
                self.add_error('password2', error)
                
    
    def clean_email(self):
        '''
        This function is used to clean the email field of registrationform.
        it check wether email is alreday taken or not.
        '''
        email = self.cleaned_data.get('email')
        
        if User.objects.filter(email = email).exists():
            self.add_error('email', 'Email already taken!')
                
                
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
    


class Loginform(forms.Form):
    username = forms.CharField(
        max_length = 30, 
        label = 'Username', 
        widget = forms.TextInput(attrs={'class':'form-control', 'autofocus':True})
    )
    passcode = forms.CharField(
        label = 'Passcode',
        strip = False,
        widget = forms.PasswordInput(attrs={'class':'form-control'})
    )
    
    
class CustomResetPasswordFrom(forms.Form):
    """
    A form that lets a user change set their password without entering the old
    password.
    this is implimented based on the default SetPasswordForm from class.
    """ 
    
    error_messages = {
        'password_mismatch': ('The two password fields didn’t match.'),
    }   
    
    new_passcode1 = forms.CharField(
        label=("New passcode"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class':'form-control'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_passcode2 = forms.CharField(
        label=("Confirm"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class':'form-control'}),
    )
    
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
    
    def clean_new_passcode2(self):
        password1 = self.cleaned_data.get('new_passcode1')
        password2 = self.cleaned_data.get('new_passcode2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )
        password_validation.validate_password(password2, self.user)
        return password2

    def save(self, commit=True):
        password = self.cleaned_data["new_passcode1"]
        self.user.set_password(password)
        if commit:
            self.user.save()
        return self.user