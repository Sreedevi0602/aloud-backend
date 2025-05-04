from django.urls import path
from . import views
from myapp.views import *

urlpatterns = [
    path('addbook/', addbook, name='addbookurl'),  
    path('booklist/', booklist, name='booklisturl'),  
    path('delete/<str:book_id>/', delete, name='delete_book'),
    path('edit/<str:book_id>/', edit, name='edit_book'),
    path('update/', update, name='update_book'),
    path('api/books/', book_list, name='book-list-url'),
    path('api/books/<str:bookid>/', views.book_detail, name='book-detail-url'),
    path('create-categories/', views.create_categories, name='create_categories'),
    path('create-category/', views.create_category, name='create_category'),
    path('category/<int:category_id>/', category_detail, name='category_detail'),
    path('assign-books/<int:category_id>/', views.assign_books_to_categories, name='assign_books_to_categories'),
    path('api/categories/', views.CategoryList.as_view(), name='category_list'),
    path('api/categories/<int:id>/', views.CategoryDetail.as_view(), name='category_details'),
    # API endpoints (React frontend)
    path('api/register/', views.RegisterUser.as_view(), name='register'),
    path('api/login/', views.LoginUser.as_view(), name='login'),
    path('api/users/', views.UserList.as_view(), name='user-list-url'),

    # HTML page for admin
    path('userlist/', views.UserListHTMLView.as_view(), name='userlisturl'),

    #To get current user in the format "Hi Username"
    path('api/current-user/', views.current_user, name='current_user'),

    path('api/user-info/', views.user_info, name='user-info'),

   

    path('api/csrf/', get_csrf_token),


]