from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create/', views.book_create, name='book_create'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('my-books/', views.my_books, name='my_books'),
    path('contact/', views.contact, name='contact'),
    path('search-borrow/', views.search_borrow, name='search_borrow'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('secure-reliable/', views.secure_reliable, name='secure_reliable'),
    path('borrow/<int:book_id>/', views.borrow_book, name='borrow_book'),
    path('secure-reliable/', views.secure_reliable, name='secure_reliable'),
    path('category/<int:category_id>/', views.category_books, name='category_books'),
path('return/<int:borrow_id>/', views.return_book, name='return_book'),
path('digital-books/', views.digital_books, name='digital_books'),
path('online-membership/', views.online_membership, name='online_membership'),
path('register/', views.register, name='register'),
path('dashboard/', views.dashboard, name='dashboard'),


]
