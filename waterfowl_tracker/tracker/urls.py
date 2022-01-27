from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('app/', views.app, name='app'),
    path('farms/', views.farms, name='farms'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('notifications/', views.NotificationView.as_view(), name='notifications'),
    path('addnew/', views.addnew, name='addnew'),  
    path('edit/<id>', views.edit, name='edit'),
    path('update/<id>', views.update, name='update'),
    path('delete/<id>', views.destroy, name='delete'),
]
