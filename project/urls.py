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
    path('docdownload/<int:pk>/', views.doc_download, name='doc_download'),
    path('addcomment/<int:pk>/', views.addcomment, name='addcomment'),
    path('kick/<int:pk>/', views.kick, name='kick'),
]
