from django.urls import path
from . import views

app_name = 'Recruit'

urlpatterns = [
    path('list/', views.list, name='list'),
    path('detail/<int:pk>/', views.detail, name='detail'),
    path('update/<int:pk>/', views.update, name='update'),
    path('apply/<int:pk>/', views.apply, name='apply'),
    path('delete/', views.delete, name='delete'),
    path('accept/', views.accept, name='accept'),
    path('deleterl/', views.deleteRecruit_Language, name="deleteRecruit_Language"),
]
