from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('farms/', views.farms, name='farms'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('notifications/', views.NotificationView.as_view(), name='notifications'),
    path('addnew/', views.addnew, name='addnew'),  
    path('edit/<int:id>', views.edit),  
    path('update/<int:id>', views.update),  
    path('delete/<int:id>', views.destroy),  
]
