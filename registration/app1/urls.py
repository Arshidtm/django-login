from django.urls import path
from . import views
urlpatterns = [

    path('', views.signup_page, name='signup'),
    path('signin/', views.signup_page, name='signup'),
    path('login/', views.login_page, name='login'),
    path('admin/',views.user_list, name='user_list'),
    path('home/', views.home_page, name='home'),
    path('home/logout/', views.logout_page, name='logout'),
    
    path('admin_home/', views.adminn, name='adminn'),
    path('admin_home/edit/<int:user_id>/', views.edit_user, name='edit_user'),
    path('admin_home/delete/<int:pk>/', views.delete_user, name='delete_user'),
    path('admin/add/', views.add_user, name='add_user'),
    path('admin/logout/', views.admin_logout, name='admin_logout'),
]