from django.urls import path
from . import views

app_name = 'Project'

urlpatterns = [
    path('create/', views.create, name='create'),
    path('list/', views.list, name='list'),
    path('detail/<int:pk>/', views.detail, name='detail'),
    path('update/<int:pk>/', views.update, name='update'),
    path('delete/', views.delete, name='delete'),
    path('deleteDocument/', views.deleteDocument, name='deleteDocument'),
    path('likeproject/<int:pk>/', views.likeproject, name='likeproject'),
    path('unlikeproject/<int:pk>/', views.unlikeproject, name='unlikeproject'),
]
