from django.urls import path, re_path
from . import views
from . import forms
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.home, name='home-page'),
    path('books/', views.listbooks, name='books-list'),
    path('books/add/', views.addbook, name='add-book'),
    path('authors/', views.listauthors, name='authors-list'),
    path('authors/add/', views.addauthor, name='add-author'),
    path('publishers/', views.listpublishers, name='publishers-list'),
    path('success/', views.success, name='success'),
    
    path('books/<bookname>/', views.bookname, name='books-name'),
    path('authors/<authorname>/', views.authorname, name='authors-name'),
    path('publishers/<pubname>/', views.publishername, name='publishers-name'),
    
    path('books/<int:year>/<int:month>/<int:date>/', views.filterbooks, name='books-year-month-date'), 
    
     
    re_path(r'^books/(?P<year>[0-9]{4})/(?P<rat>[0-9]{1}[.][0-9]{1})/$', views.ratingbooks, name='books-rating'),
    re_path(r'^books/book/(?:id-(?P<bookid>\d+)/)?$', views.idbook, name='book-id'),    # Good implimentation of nesting arguments
    
    path('vichel/add/', views.addvichel, name='add-vichel'),
    
    path('signup/', views.signup, name='signup-path'),
    path('signin/', views.signin, name='signin-path'),
    path('signout/', views.signout, name='signout-path'),
    
    path('reset-password/', auth_views.PasswordResetView.as_view(template_name = 'password_reset_email.html'), name = 'password_reset'),
    path('reset-password-sent/', auth_views.PasswordResetDoneView.as_view(template_name = 'password_reset_email_sent.html'), name = 'password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name = 'password_reset_confirm.html', form_class = forms.CustomResetPasswordFrom), name = 'password_reset_confirm'),
    path('reset-password-complete/', auth_views.PasswordResetCompleteView.as_view(template_name = 'password_reset_complete.html'), name = 'password_reset_complete'),
]