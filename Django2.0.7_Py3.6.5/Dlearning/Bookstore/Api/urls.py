from django.urls import path
from . import views

from rest_framework.authtoken import views as rest_auth_views

urlpatterns = [
    path('bookstore/allbooks/', views.allbooks, name = 'all-books'),
    path('bookstore/allbooks/apiview/', views.allbooksapiview.as_view(), name = 'all-books-api-view'),
    path('bookstore/allauthors/', views.allauthors, name = 'all-authors'),
    path('bookstore/allpublishers/', views.allpublishers, name = 'all-publishers'),
    
    path('bookstore/author/<str:authname>/update/', views.updateauthor, name='author-update'),
    path('bookstore/book/create/', views.createbook, name='book-create'),
    path('bookstore/book/<str:bookname>/delete/', views.deletebook, name='book-delete'),
    
    path('bookstore/auth/token/', rest_auth_views.obtain_auth_token, name = 'obtain-token')
]