from django.urls import path
from . import views

urlpatterns = [
    path('notifications/',views.notifications,name='notifications'),
    path('delete-notification/<int:pk>/', views.delete_notification, name='delete-notification'),
]