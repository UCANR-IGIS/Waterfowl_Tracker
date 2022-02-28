from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('app/', views.app, name='app'),
    path('farms/', views.farms, name='farms'),
    path('notification/', views.notifications, name='notification'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    #path('notifications/', views.NotificationView.as_view(), name='notifications'),
    path('notifications/', views.NotificationView, name='notifications'),
    path('addnew/', views.addnew, name='addnew'),  
    path('edit/<id>', views.edit, name='edit'),
    path('update/<id>', views.update, name='update'),
    path('delete/<id>', views.destroy, name='delete'),
    path('editNotification/<id>', views.editNotification, name='editNotification'),
    path('updateNotification/<id>', views.updateNotification, name='updateNotification'),
    path('deleteNotification/<id>', views.destroyNotification, name='deleteNotification'),
    path('farm_json/', views.farm_json, name='farm_json'),
    path('buffer_json/', views.buffer_json, name='buffer_json')
]
