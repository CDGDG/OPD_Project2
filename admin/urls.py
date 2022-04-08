from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = "Admin"

urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('', views.adminlogin, name='adminlogin'),
    path('notice/list/', views.noticelist, name='noticelist'),
    path('notice/write/', views.noticewrite, name='noticewrite'),
    path('notice/delete/', views.noticedelete, name='noticedelete'),
    path('notice/detail/<int:pk>/', views.noticedetail, name='noticedetail'),
    path('checkuserid/',views.check_userid, name="check_userid"),
    path('resetpassword/',views.reset_password, name="resetpassword"),
    
]
