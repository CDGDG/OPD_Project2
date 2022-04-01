from django.urls import path
from . import views

app_name = 'Company'

urlpatterns = [
    path('list/', views.list, name='list'),
    path('detail/<int:pk>/', views.detail, name='detail'),
    path('update/<int:pk>/', views.update, name='update'),
    path('delete/<int:pk>/', views.delete, name='delete'),
    path('join/', views.join, name='join'),
    path('login/', views.login, name='login'),
]
