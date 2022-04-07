from django.urls import path
from . import views

app_name = 'Company'

urlpatterns = [
    path('list/', views.list, name='list'),
    path('detail/<int:pk>/', views.detail, name='detail'),
    path('update/<int:pk>/', views.update, name='update'),
    path('delete/', views.delete, name='delete'),
    path('join/', views.join, name='join'),
    path('check_id/',views.check_id, name='check_id'),
    path('follow/', views.follow, name='follow'),
]
