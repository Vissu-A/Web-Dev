from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404, get_list_or_404
from django.views import View

from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest, Http404, HttpResponseNotFound
from django.urls import reverse
from .models import Book, Author, Publisher
from django.db.models import Q
import datetime

from django.views.decorators.http import require_http_methods, require_GET, require_POST, require_safe, condition, last_modified, etag
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.gzip import gzip_page
from django.views.decorators.vary import vary_on_headers, vary_on_cookie
from django.views.decorators.cache import cache_control, never_cache

'''
Be careful with the order of decorators. When condition decorator returns a conditional response, any decorators 
below it will be skipped and won’t apply to the response. Therefore, any decorators that need to apply to both 
the regular view response and a conditional response must be above condition decorator.
'''


from Bookstore import forms
from django.contrib import messages

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password, is_password_usable

from .tasks import sendingmail

def authorcondition(request, authorname):
    return Book.objects.filter(author__name = authorname).latest('pubdate').pubdate
    


@require_http_methods(['GET','POST'])
@cache_control(must_revalidate = True, max_age = 60 * 10)
def home(request):
    print(request.user)
    print(request.session)    # <django.contrib.sessions.backends.db.SessionStore object at 0x000001C71BB22828>
    request.session.set_test_cookie()   # Test out whether your browser supports cookies.
    
    return render(request, 'base.html', {'request':request})

@require_GET
@gzip_page
@vary_on_headers('User-Agent', 'Cookie')
@login_required(login_url = 'signin-path', redirect_field_name='next')
def listbooks(request):
    print(request.session.items())   # dict_items([('_auth_user_backend', 'django.contrib.auth.backends.ModelBackend'), ('_auth_user_hash', 'b72b4f84336ad481ec23917e4e696f3911564a86'), ('_auth_user_id', '1')])
    print(request.session.keys())    # dict_keys(['_auth_user_id', '_auth_user_backend', '_auth_user_hash'])
    print(request.session['_auth_user_id'])
    print(request.session.get('_auth_user_id'))
    print(request.session.get('_auth_user_data', 'Key not exists'))
    print('Current user: ', request.user)
    # print(request.session.get_session_cookie_age())   # New function to get session cookie expiry in Django-3 
    if request.session.test_cookie_worked():    # Returns either True or False, depending on whether the user’s browser accepted the test cookie.
        print("Test cookie is worked...")
        request.session.delete_test_cookie()    # Deletes the test cookie.
    
    QuerySet = Book.objects.all()
    
    return render(request, 'booklist.html', {'data':QuerySet})

@require_safe
@vary_on_headers('user-agent', 'cookie')
@login_required(login_url = 'signin-path', redirect_field_name='next')
def listauthors(request):
    QuerySet = Author.objects.all()
    
    return render(request, 'authorlist.html', {'data':QuerySet})    

@require_GET
@vary_on_cookie
@login_required(login_url = 'signin-path', redirect_field_name='next')
def listpublishers(request):
    request.session.clear_expired()
    # request.session.set_expiry(60 * 2)
    QuerySet = Publisher.objects.all()
    
    return render(request, 'publisherlist.html', {'data':QuerySet})

@require_GET
@login_required(login_url = 'signin-path', redirect_field_name='next')
@condition(last_modified_func=authorcondition, etag_func = None)
def authorname(request, authorname):
    
    '''
    We are implimented last_modified_func condition on this view. when we request perticular author resourse
    1st time it will give the 200 status code. for the second request it will check the last_modified_func, if 
    the requested resources are not modified since the time specified in the request it will give 304 status code
    which means HttpResponseNotModified.
    '''
    
    print('=========================Author name===============================')
    print(authorname)
    print('===========================END===================================')
    
    QuerySet = Author.objects.get(name = authorname).book_set.all()
    
    return render(request, 'booklist.html', {'data':QuerySet})

@never_cache
@login_required(login_url = 'signin-path', redirect_field_name='next')
def publishername(request, pubname):
    
    print('=========================Publisher name===============================')
    print(pubname)
    print('===========================END===================================')
    
    #QuerySet = Publisher.objects.get(name = pubname).book_set.all()
   
    QuerySet = get_object_or_404(Publisher, name = pubname).book_set.all()
        
    return render(request, 'booklist.html', {'data':QuerySet})

@login_required(login_url = 'signin-path', redirect_field_name='next')
def bookname(request, bookname):
    
    print('=========================Book name===============================')
    print(bookname)
    print('===========================END===================================')
    
    QuerySet = Book.objects.filter(name = bookname)
    
    if QuerySet:
        return HttpResponse(QuerySet)
        
    else:
        raise Http404('No book found with book name')  # to server custom 404.html set DEBUG = False in settings.py
        # return HttpResponseNotFound('nO BOOK')
        #return HttpResponseRedirect(reverse('books-list', args=None))
        
@login_required(login_url = 'signin-path', redirect_field_name='next')
def filterbooks(request, year, month, date):
    print('===================URL Parameters===================')
    print('year is: '+str(year)+' month is: '+str(month)+' date is: '+str(date))
    print('===================URL Parameters===================')
    
    #QuerySet = Book.objects.filter(Q(pubdate__year = year) & Q(pubdate__month = month) & Q(pubdate__day = date))
    QuerySet = Book.objects.filter(pubdate=datetime.date(year,month,date))
    
    return HttpResponse(QuerySet)

@require_GET
@cache_control(must_revalidate = True ,max_age = 60 * 10)
@login_required(login_url = 'signin-path', redirect_field_name='next')
def ratingbooks(request, year, rat):
    # QuerySet = Book.objects.filter(Q(pubdate__year = year) & Q(rating=rat))
    
    QuerySet = get_list_or_404(Book, Q(pubdate__year = year) & Q(rating=rat))
    
    return render(request ,'booklist.html', {"data":QuerySet})

@login_required(login_url = 'signin-path', redirect_field_name='next')
def idbook(request, bookid):
    
    book = Book.objects.get(pk=bookid)
    
    return HttpResponse('Book Name: '+book.name+'<br>'+'Book Price: '+str(book.price)+'<br>'+'Book Rating: '+str(book.rating))



@login_required(login_url = 'signin-path', redirect_field_name='next')
@permission_required('Bookstore.add_Book', login_url = 'signin-path', raise_exception = True)
def addbook(request):
    if request.method == 'POST':
        form  = forms.Bookform(request.POST)
        
        if form.is_bound:
            if form.is_valid():
                form.save()
                # author = form.cleaned_data['author']
                # publisher = form.cleaned_data['publisher']
                # bname = form.cleaned_data['bookname']
                # pgno = form.cleaned_data['pagecnt']
                # price = form.cleaned_data['price']
                # rating = form.cleaned_data['rating']
                # date = form.cleaned_data['pdate']
            
                # aut = get_object_or_404(Author, name = author)
                # pub = get_object_or_404(Publisher, name = publisher)
            
                # ath = Author.objects.get(name = author)
            
                # book  = Book(publisher = pub, name = bname, pages = pgno, price = price, rating = rating, pubdate = date)
                # book.save()
                # ath.book_set.add(book)
            
                form = forms.Bookform()
            
                messages.success(request, 'Book added successfully')
            
    else:
        form = forms.Bookform()
        
    return render(request, 'addbook.html', {'form':form})

@login_required(login_url = 'signin-path', redirect_field_name='next')
def addauthor(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = forms.authorform(request.POST)
            
            if form.is_bound:                              # tell you whether the form has data bound to it or not
                
                if form.is_valid():                         
                    name = form.cleaned_data['authname']
                    email = form.cleaned_data['email']
                    age = form.cleaned_data['age']
            
                    author = Author.objects.create(name = name, email=email, age=age)  # to create and save obj in single step use create() method

                    return HttpResponseRedirect(reverse('success'))
        else:
            form = forms.authorform()
            
        return render(request, 'addauthor.html', {'form':form})
    
    else:
        return redirect('%s?next=%s' % (reverse('signin-path'), request.path))
        

def success(request):
    msg = 'Author added successfully'
    return render(request, 'success.html', {'message':msg})



def addvichel(request):
    
    if request.method == 'POST':
        form = forms.Vichelform(request.POST, request.FILES)
        
        if form.is_bound:                              # tell you whether the form has data bound to it or not
            if form.is_valid():
                form.save()
                
                form = forms.Vichelform()
            
                messages.success(request, 'Vichel added successfully')
    
    else:
        form = forms.Vichelform()
        
    return render(request, 'addvichel.html', {'form' : form})


def signup(request):
    # import pdb; pdb.set_trace()
    if request.user.is_authenticated:
        return redirect('home-page')
    
    else:
        if request.method == 'POST':
            form = forms.CustomUserRegistrationForm(request.POST)
        
            if form.is_bound:
                if form.is_valid():
                    username = form.cleaned_data['username']
                    passcode = form.cleaned_data['password1']
                    emailid = form.cleaned_data['email']
                    
                    form.save()
                
                    form = forms.CustomUserRegistrationForm()
                  
                    sendingmail.delay(username, passcode, emailid)
                    messages.success(request, 'User created successfully')
                    return redirect('signin-path')
        else:
            form  = forms.CustomUserRegistrationForm()
        
        return render(request, 'signup.html', {'form':form})


# def signin(request):
       
#     #This is implimented by using default AuthenticationForm
       
#     if request.method == 'POST':
#         form = AuthenticationForm(request = request, data = request.POST)
        
#         if form.is_bound:
#             if form.is_valid():
#                 username = form.cleaned_data['username']
#                 password = form.cleaned_data.get('password')
                
#                 user = authenticate(request, username=username, password=password)
        
#                 if user is not None:
#                     login(request, user)
#                     return redirect('books-list')
            
#     else:
#         form = AuthenticationForm()
        
#     return render(request, 'login.html', {'form':form})


def signin(request):
    # import pdb; pdb.set_trace()
    if request.user.is_authenticated:
        return redirect('home-page')
    
    else:
        if request.method == 'POST':
            form = forms.Loginform(request.POST)
        
            username = request.POST['username']
            passcode = request.POST.get('passcode')
        
            if username and passcode:
            
                if not User.objects.filter(username=username).exists():    # if we use get instead of filter it will give DoesNotExists exception if user not there in the database.
                    form.add_error('username', 'There is no user with the name '+username)
                
                else:
                    user = User.objects.get(username=username)
                
                    if not check_password(passcode, user.password):
                        form.add_error('passcode', 'Invalid Passcode!')
                        
                    else:
                        user = authenticate(request=request, username=username, password=passcode)
                    
                        if user is not None:
                            login(request, user)
                            if request.POST.get('next'):
                                return redirect(request.POST.get('next'))    # 'next' is for redirecting to @login_required() specified url, if no next then redirects to 'books-list' after user logedin successfully.
                                # or
                                # return HttpResponseRedirect(request.POST.get('next'),'/accounts/loggedin')
                            else:
                                return redirect('home-page')
        else:
            form = forms.Loginform()
        
        return render(request, 'login.html', {'form':form})
    
    
def signout(request):
    logout(request)
    messages.info(request, 'You have logedout successfully')
    return redirect('signin-path')
