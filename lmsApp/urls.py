from django.contrib import admin
from django.urls import path,include
from . import views
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.home, name="home-page"),
    path('login',views.login_page,name='login-page'),
    path('register',views.userregister,name='register-page'),
    path('save_register',views.save_register,name='register-user'),
    path('user_login',views.login_user,name='login-user'),
    path('home',views.home,name='home-page'),
    path('logout',views.logout_user,name='logout'),
    path('profile',views.profile,name='profile-page'),
    path('update_password',views.update_password,name='update-password'),
    path('update_profile',views.update_profile,name='update-profile'),
    path('users',views.users,name='user-page'),
    path('manage_user',views.manage_user,name='manage-user'),
    path('manage_user/<int:pk>',views.manage_user,name='manage-user-pk'),
    path('view_user/<int:pk>',views.view_user,name='view-user-pk'),
    path('save_user',views.save_user,name='save-user'),
    path('delete_user/<int:pk>',views.delete_user,name='delete-user'),
    path('category',views.category,name='category-page'),
    path('manage_category',views.manage_category,name='manage-category'),
    path('manage_category/<int:pk>',views.manage_category,name='manage-category-pk'),
    path('view_category/<int:pk>',views.view_category,name='view-category-pk'),
    path('save_category',views.save_category,name='save-category'),
    path('delete_category/<int:pk>',views.delete_category,name='delete-category'),
    path('book',views.books,name='book-page'),
    path('manage_book',views.manage_book,name='manage-book'),
    path('manage_book/<int:pk>',views.manage_book,name='manage-book-pk'),
    path('view_book/<int:pk>',views.view_book,name='view-book-pk'),
    path('save_book',views.save_book,name='save-book'),
    path('delete_book/<int:pk>',views.delete_book,name='delete-book'),
    path('borrows',views.borrows,name='borrow-page'),
    path('manage_borrow',views.manage_borrow,name='manage-borrow'),
    path('manage_borrow/<int:pk>',views.manage_borrow,name='manage-borrow-pk'),
    path('view_borrow/<int:pk>',views.view_borrow,name='view-borrow-pk'),
    path('save_borrow',views.save_borrow,name='save-borrow'),
    path('delete_borrow/<int:pk>',views.delete_borrow,name='delete-borrow'),
    path('user_borrows',views.user_borrows,name='user_borrow-page'),
    path('', views.product_search, name='product-search'),
    path('autocomplete/', views.ProductAutocomplete.as_view(), name='product-autocomplete'),
]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
