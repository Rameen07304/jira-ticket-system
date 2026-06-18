from django.urls import path
from . import views

urlpatterns = [
    path('homepage/', views.home_view, name='homepage'),
    path('home/', views.home, name='home'),
    path('tickets/', views.ticket_list, name='ticket_list'),
    path('user_ticket_list/', views.user_ticket_list, name='user_ticket_list'),
    path('tickets/update/<int:ticket_id>/', views.update_ticket_status, name='update_ticket_status'),
    path('tickets/priority/<int:ticket_id>/', views.update_ticket_priority, name='update_ticket_priority'),
    path('tickets/delete/<int:ticket_id>/', views.delete_ticket, name='delete_ticket'),
]