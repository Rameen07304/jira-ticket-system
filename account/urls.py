from django.urls import path
from . import views 

urlpatterns = [
    
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('update/', views.update_profile_view, name='update_profile'),  # shows form
    path('update/ajax/', views.update_profile_ajax, name='update_profile_ajax'),
    path('delete/', views.delete_profile, name='delete_profile'),
    
   path('user/<int:user_id>/view/', views.view_user, name='view_user'),
    path('user/<int:user_id>/edit/', views.edit_user, name='edit_user'),
    path('user/<int:user_id>/delete/', views.delete_user, name='delete_user'),
]