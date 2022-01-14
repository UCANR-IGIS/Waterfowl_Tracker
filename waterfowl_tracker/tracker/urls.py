from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('notifications/', views.NotificationView.as_view(), name='notifications'),
]
