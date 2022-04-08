from django.urls import path
from . import views

app_name = "Admin"

urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('', views.adminlogin, name='adminlogin'),
    path('notice/list/', views.noticelist, name='noticelist'),
    path('notice/write/', views.noticewrite, name='noticewrite'),
    path('notice/delete/', views.noticedelete, name='noticedelete'),
    path('notice/detail/<int:pk>/', views.noticedetail, name='noticedetail'),
]